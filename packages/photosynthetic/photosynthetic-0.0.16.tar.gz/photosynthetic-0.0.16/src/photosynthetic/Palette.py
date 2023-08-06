import json
import math
import os

from .PaletteImage import PaletteImage

from PIL import Image, ImageDraw, ImageFont
from os.path import join
from skimage.color import rgb2lab, lab2rgb
from skimage.future import graph
from skimage import color as skicolor, segmentation, color, filters
from skimage.io import imsave
import numpy as np

from .Colors import primary_colors
from .Debug import Debug
from matplotlib import pyplot as plt
from skimage.measure import regionprops

# I hate this package
import imageio.core.util

def ignore_warnings(*args, **kwargs):
    pass

imageio.core.util._precision_warn = ignore_warnings


class Palette():
    superpixel_boundary_image = []
    file_name = ''

    primary_colors = primary_colors

    def __init__(self, image_filepath):

        self.base_colors = None
        self.STEP_DECREMENT = None
        self.TARGET_PALETTE_SIZE = None
        self.ADJACENT_REGION_DISTANCE_THRESHOLD = None
        self.TANGENTIAL_REGION_DISTANCE_THRESHOLD = None
        self.SUPERPIXEL_METHOD = None
        self.SEGMENTS_COUNT = None
        self.MIN_DISTANCE_THRESHOLD = None
        self.OUTPUT_DIR = None

        self.palette_image = None

        self.image_filepath = image_filepath
        self.file_name = os.path.basename(image_filepath)
        self.debug = Debug(5)

        self.configure()

    def configure(self,
                  target_palette_size=6,
                  tangential_region_distance_threshold=25,
                  adjacent_region_distance_threshold=5,
                  step_decrement=0.5,
                  superpixel_method='slic',
                  segments_count=1000,
                  min_distance_threshold=15,
                  output_dir='',
                  counter=1,
                  debug_level=5

                  ):
        """

        @param segments_count:
        @param superpixel_method:
        @param debug_level:
        @param target_palette_size: The algorithm will attempt to extract at least this many unique colors from the
                                    image. Final palette may exceed this number. Just drop the extra off the end if
                                    you need exactly this number. The algoritmhm will sacrifice accuracy to achieve this
                                    number of colors
        @param tangential_region_distance_threshold: The maximum distance apart two colors can be before we consider
                                                     them the same palette entry
        @param adjacent_region_distance_threshold: The maximum distance apart two colors can be before we consider them
                                                   the same palette entry
        @param step_decrement: If we don't have a palette of at least MINIMUM_PALETTE_SIZE then we will decrease the
                               necessary DISTANCE_THRESHOLD by the below amount until we do. Increase this for a faster,
                               but less accurate, result.
        @return: Palette
        """

        self.set_base_colors()

        self.TARGET_PALETTE_SIZE = target_palette_size
        self.TANGENTIAL_REGION_DISTANCE_THRESHOLD = tangential_region_distance_threshold
        self.ADJACENT_REGION_DISTANCE_THRESHOLD = adjacent_region_distance_threshold
        self.STEP_DECREMENT = step_decrement
        self.SUPERPIXEL_METHOD = superpixel_method
        self.SEGMENTS_COUNT = segments_count
        self.MIN_DISTANCE_THRESHOLD = min_distance_threshold
        self.counter = counter

        if output_dir == '' :
            self.OUTPUT_DIR = os.path.join('resources', 'output')

        self.debug.debug_level = debug_level

        return self

    def set_base_colors(self):
        this_dir, this_filename = os.path.split(__file__)
        colors_path = join(this_dir, 'colors.json')
        with open(colors_path, 'r') as f:
            colors = json.loads(f.read())

        self.base_colors = colors['data']


    def calculate_color_de(self, c1, c2):
        """

        Calculate the delta of two colors in L*a*b* space

        @param c1:
        @param c2:
        @return:
        """
        l1 = c1[0]
        l2 = c2[0]

        a1 = c1[1]
        a2 = c2[1]

        b1 = c1[2]
        b2 = c2[2]

        # Convert LAB to LCH

        # Lightness Values Stay the Same
        L_star1 = l1
        L_star2 = l2

        C_star1 = math.sqrt((a1 ** 2) + (b1 ** 2))
        C_star2 = math.sqrt((a2 ** 2) + (b2 ** 2))

        h_arctan1 = np.rad2deg(math.atan2(b1, a1))
        if h_arctan1 >= 0:
            H_star1 = h_arctan1
        else:
            H_star1 = h_arctan1 + 360

        h_arctan2 = np.rad2deg(math.atan2(b2, a2))
        if h_arctan2 >= 0:
            H_star2 = h_arctan2
        else:
            H_star2 = h_arctan2 + 360

        # Lightness Phrase
        Delta_L_mark = L_star2 - L_star1
        L_Bar_mark = (L_star1 + L_star2) / 2

        S_L = 1 + ((0.015 * ((L_Bar_mark - 50) ** 2)) / (math.sqrt(20 + ((L_Bar_mark - 50) ** 2))))
        K_L = 1

        lightness_phrase = (Delta_L_mark / (K_L * S_L))
        # print("Lightness Phrase : {0}".format(lightness_phrase))

        # Chroma Phrase
        C_star_bar = (C_star1 + C_star2) / 2

        c7_phrase = (1 - math.sqrt((C_star_bar ** 7) / ((C_star_bar ** 7) + (25 ** 7))))
        a_mark1 = a1 + ((a1 / 2) * c7_phrase)
        a_mark2 = a2 + ((a2 / 2) * c7_phrase)

        C_mark1 = math.sqrt((a_mark1 ** 2) + (b1 ** 2))
        C_mark2 = math.sqrt((a_mark2 ** 2) + (b2 ** 2))

        Delta_C_mark = C_mark2 - C_mark1
        C_bar_mark = (C_mark1 + C_mark2) / 2

        K_C = 1
        S_C = 1 + (0.045 * C_bar_mark)

        chroma_phrase = (Delta_C_mark / (K_C * S_C))
        # print("Chroma Phrase : {0}".format(chroma_phrase))

        # Hue Phrase
        polar_compensation = 2 * math.pi
        h_mark_1 = math.atan2(b1, a_mark1)
        h_mark_2 = math.atan2(b2, a_mark2)

        delta_h_mark_check = np.rad2deg(abs(h_mark_2 - h_mark_1))
        delta_h_mark = h_mark_2 - h_mark_1
        if delta_h_mark_check <= 180:
            pass
        elif delta_h_mark_check > 180 and h_mark_2 <= h_mark_1:
            delta_h_mark += polar_compensation
        elif delta_h_mark > 180 and h_mark_2 > h_mark_1:
            delta_h_mark -= polar_compensation

        Delta_H_mark = 2 * math.sqrt(C_mark1 * C_mark2) * math.sin(delta_h_mark / 2)

        if c1 == 0 or c2 == 0:
            Delta_H_mark = 0

        H_bar_mark = (h_mark_1 + h_mark_2) / 2
        h_abs_diff = np.rad2deg(abs(h_mark_1 - h_mark_2))
        if h_abs_diff <= 180:
            H_bar_mark = (h_mark_1 + h_mark_2) / 2
        elif h_abs_diff > 180 and (h_mark_1 + h_mark_2) < 360:
            H_bar_mark = (h_mark_1 + h_mark_2 + polar_compensation) / 2
        elif h_abs_diff > 180 and (h_mark_1 + h_mark_2) >= 360:
            H_bar_mark = (h_mark_1 + h_mark_2 - polar_compensation) / 2

        T_var = (1 -
                 (0.17 * math.cos(H_bar_mark - np.deg2rad(30))) +
                 (0.24 * math.cos(2 * H_bar_mark)) +
                 (0.32 * math.cos((3 * H_bar_mark) + np.deg2rad(6))) +
                 (0.20 * math.cos((4 * H_bar_mark) - np.deg2rad(63)))
                 )

        K_H = 1
        S_H = 1 + (0.015 * C_bar_mark * T_var)

        hue_phrase = (Delta_H_mark / (K_H * S_H))

        # print("Hue Phrase : {0}".format(hue_phrase))

        # Hue Rotation Phrase
        C_bar_mark_7 = C_bar_mark ** 7
        R_T = -2 * math.sqrt((C_bar_mark_7 / (C_bar_mark_7 + 25 ** 7))) * math.sin(
            np.deg2rad(60) * math.exp(-1 * (((H_bar_mark - np.deg2rad(275)) / np.deg2rad(25)) ** 2)))

        Delta_E_2000 = math.sqrt(
            lightness_phrase ** 2 + chroma_phrase ** 2 + hue_phrase ** 2 + (R_T * chroma_phrase * hue_phrase))
        # print("Distance : {}".format(Delta_E_2000))

        # distance = skicolor.deltaE_ciede2000([l1, a1, b1], [l2, a2, b2])
        # print("Distance : {}".format(distance))

        # quit()

        return Delta_E_2000

    def weight_mean_color(self, graph, src, dst, n):
        """Callback to handle merging nodes by recomputing mean color.

        The method expects that the mean color of `dst` is already computed.

        Parameters
        ----------
        graph : RAG
            The graph under consideration.
        src, dst : int
            The vertices in `graph` to be merged.
        n : int
            A neighbor of `src` or `dst` or both.

        Returns
        -------
        resources : dict
            A dictionary with the `"weight"` attribute set as the absolute
            difference of the mean color between node `dst` and `n`.
        """

        l1 = graph.nodes[dst]['mean color'][0]
        a1 = graph.nodes[dst]['mean color'][1]
        b1 = graph.nodes[dst]['mean color'][2]

        l2 = graph.nodes[n]['mean color'][0]
        a2 = graph.nodes[n]['mean color'][1]
        b2 = graph.nodes[n]['mean color'][2]

        diff = self.calculate_color_de([l1, a1, b1], [l2, a2, b2])

        diff = np.linalg.norm(diff)
        return {'weight': diff}

    def merge_mean_color(self, graph, src, dst):
        """Callback called before merging two nodes of a mean color distance graph.

        This method computes the mean color of `dst`.

        Parameters
        ----------
        graph : RAG
            The graph under consideration.
        src, dst : int
            The vertices in `graph` to be merged.
        """

        graph.nodes[dst]['total color'] += graph.nodes[src]['total color']
        graph.nodes[dst]['pixel count'] += graph.nodes[src]['pixel count']
        graph.nodes[dst]['mean color'] = (graph.nodes[dst]['total color'] /
                                          graph.nodes[dst]['pixel count'])

    def superpixel(self):
        image = PaletteImage(self.image_filepath)
        self.palette_image = image
        og_image = image
        slic_segments = image.get_superpixel_segments(segments=self.SEGMENTS_COUNT, algo=self.SUPERPIXEL_METHOD)

        lab_image = rgb2lab(image.image_matrix)

        adjecency_graph = graph.rag_mean_color(lab_image, slic_segments)
        merged_adjecency_graph = graph.merge_hierarchical(slic_segments, adjecency_graph, thresh=self.ADJACENT_REGION_DISTANCE_THRESHOLD,
                                                          rag_copy=False,
                                                          in_place_merge=True,
                                                          merge_func=self.merge_mean_color,
                                                          weight_func=self.weight_mean_color)
        image = skicolor.label2rgb(merged_adjecency_graph, image.image_matrix, kind='avg', bg_label=0)

        # image = segmentation.mark_boundaries(image, merged_adjecency_graph, (0, 0, 0), mode='inner')

        # edges = filters.sobel(color.rgb2gray(image))
        # g = graph.rag_boundary(slic_segments, edges)
        #
        # graph.show_rag(slic_segments, g, image)
        # plt.title('RAG after hierarchical merging')
        # plt.figure()
        # out = color.label2rgb(merged_adjecency_graph, image, kind='avg', bg_label=0)
        # plt.imshow(out)
        # plt.title('Final segmentation')
        # plt.savefig('thing2.png')

        # plt.show()
        # quit()
        self.superpixel_boundary_image = image

        lab_intensity_image = rgb2lab(image)

        props = regionprops(merged_adjecency_graph, intensity_image=image[:, :, 0])

        self.props = props
        self.mag = merged_adjecency_graph


        all_colors = {}
        for s, segment in enumerate(merged_adjecency_graph):
            if s + 1 > len(props):
                break

            # imsave('thing3.png', lab2rgb(props[s]._intensity_image))
            pixel_area = props[s].area
            # print(pixel_area)

            x = round(props[s].centroid[0])
            y = round(props[s].centroid[1])
            l = lab_intensity_image[x][y][0]
            a = lab_intensity_image[x][y][1]
            b = lab_intensity_image[x][y][2]

            current_color = (l, a, b)

            if current_color == (56.484817321085586, -16.15765543304859, -23.754401116849834):
                print(pixel_area, props[s].centroid, vars(props[s]))
                # quit()



            if current_color in all_colors:
                all_colors[current_color] += pixel_area
            else:
                all_colors[current_color] = pixel_area

        return all_colors

    def extract(self, dominant_colors=False, callback=lambda payload: payload):
        """
        Now that we have all the dominant colors
        in the image we can begin to compare
        them against each other, so we can extract
        the truly unique ones into a single palette
        """

        if not dominant_colors:
            dominant_colors = self.superpixel()




        sorted_dominant_colors = Palette.sort_dict(dominant_colors)

        palette_score = {}
        total_area = 0
        # print(sorted_dominant_colors)
        for c in sorted_dominant_colors:

            color = c[0]
            score = c[1]

            # if color == (56.484817321085586, -16.15765543304859, -23.754401116849834):
            # print(score)
            # quit()

            total_area += score

            # if color == (52.388426743374666, -4.262454458777931, -2.673994734945495):
            #     print('yep', score)
            #     quit()

            # See if we have come across a similar color than this one in the palette so far
            existing_color = self.color_diff(color, score, palette_score, dominant_colors)

            # if color == (11.986346097618384, -10.460822727749647, -1.1409583783878408):
            #     print(color, existing_color)
            #     quit()

            if not existing_color:
                # If we have not come across this color before, initialize it in the palette and/or increment it
                # self.debug.infoself.debug.info(existing_color)
                # If the color is not in our dict, init the color in the palette
                palette_score[color] = score
            else:
                new_color = existing_color[0]

                if new_color in palette_score:
                    palette_score[new_color] += score
                else:
                    palette_score[new_color] = score




        palette_score = Palette.sort_dict(palette_score)

        # print(palette_score)


        # print("===== TOP COLORS : {0} =====".format(self.TANGENTIAL_REGION_DISTANCE_THRESHOLD))
        self.debug.info(palette_score)

        hex_colors = []
        for color in palette_score:
            color = color[0]
            color = self.getHexCode(color)
            hex_colors.append(color)

        # payload = {
        #     "c": "e",
        #     "palette": hex_colors
        # }
        #
        # callback(payload)
        # time.sleep(0.1)

        # If we don't find at least self.MINIMUM_PALETTE_SIZE unique colors
        # then reduce the threshold the distance algorithm must meet to determine a
        # unique color
        # This may happen in the event where an image has very limited color diversity
        if len(palette_score) < self.TARGET_PALETTE_SIZE and self.TANGENTIAL_REGION_DISTANCE_THRESHOLD > self.MIN_DISTANCE_THRESHOLD:
            self.TANGENTIAL_REGION_DISTANCE_THRESHOLD -= self.STEP_DECREMENT
            return self.extract(dominant_colors, callback=callback)

        # self.save_result_image(palette_score)
        self.write_palette_to_image(palette_score)

        if len(self.superpixel_boundary_image) > 0:
            file_path = join('resources/', 'superpixel-' + self.file_name)
            # imsave(file_path, self.superpixel_boundary_image)

            # cloud = Cloud()
            # cloud.client.upload_file(ExtraArgs={'ACL': 'public-read'}, Key='public/images/superpixel/' + self.file_name,
            #                          Bucket=cloud.bucket, Filename='/tmp/superpixel-' + self.file_name)

            # print(file_path)

        meta = {
            "tints": {},
            "shades": {},
            "primary_colors": {},
            "palette_score": {}
        }
        hex_colors = []
        for color in palette_score:
            lab_color = color[0]
            color_score = color[1]
            hex_color = self.getHexCode(lab_color)
            hex_colors.append(hex_color)

            variants = self.get_variants(lab_color)

            primary_color = {}
            primary_distance = 100000

            for base_color in self.base_colors:

                nhex_color = base_color['attributes']['hex']

                base_lab_color = self.hex_to_lab(nhex_color)

                distance = self.calculate_color_de(lab_color, base_lab_color)
                if distance < primary_distance:
                    primary_distance = distance
                    primary_color = base_color['attributes']

            # print(color_score / total_area, hex_color, primary_color, primary_distance)

            if (primary_distance < 15 and color_score / total_area > .1) or primary_distance < 2:

                if hex_color not in meta["primary_colors"]:
                    meta["primary_colors"][hex_color] = []
                for c in primary_color['related']:
                    meta["primary_colors"][hex_color].append(c['color']['name'])
            meta["shades"][hex_color] = []
            meta["tints"][hex_color] = []

            meta["shades"][hex_color] = variants["shades"]
            meta["tints"][hex_color] = variants["tints"]
            meta["palette_score"][hex_color] = int(color_score)

        retval = {
            "palette": hex_colors,
            "meta": meta
        }

        return retval

    # Generates tints and shades for a given color in the LAB space, returns Hex Values
    def get_variants(self, lab_color, step=5):

        shades = []
        tints = []

        for i in range(-3, 4):

            new_lightness = lab_color[0] + (i * step)

            if new_lightness < 0:
                new_lightness = 0
            elif new_lightness > 100:
                new_lightness = 100

            new_lab_color = (new_lightness, lab_color[1], lab_color[2])
            new_hex = self.getHexCode(new_lab_color)

            if i < 0:
                shades.append(new_hex)
            elif i > 0:
                tints.append(new_hex)

        return {
            "shades": shades,
            "tints": tints,
        }

    def save_result_image(self, palette):

        im = Image.new('RGB', (math.floor(self.palette_image.width * 2), self.palette_image.height))

        square_size = math.floor(50)
        offset = 0
        # Write the superpixel result image to file
        if len(self.superpixel_boundary_image) > 0:

            file_path = join('resources/', 'superpixel-' + self.file_name)
            # imsave(file_path, self.superpixel_boundary_image)
            im2 = Image.open(self.image_filepath)
            im.paste(im2)
            im2 = Image.open(file_path)

            props = self.props

            for s, segment in enumerate(self.mag):
                if s + 1 > len(props):
                    break
                # print(pixel_area)

                x = round(props[s].centroid[0])
                y = round(props[s].centroid[1])
                d2 = ImageDraw.Draw(im2)
                font = ImageFont.truetype("arial.ttf", 11)

                if props[s].label == 27 or props[s].label == 6:

                    d2.text((x, y), "{}".format(props[s].label), fill=(255, 255, 255), font=font)
            im.paste(im2, (self.palette_image.width, 0))


            d1 = ImageDraw.Draw(im)
            font = ImageFont.truetype("arial.ttf", 18)
            d1.text((self.palette_image.width + 20, im2.height), "Target Palette Size: {}".format(self.TARGET_PALETTE_SIZE), fill=(255, 255, 255), font=font)
            d1.text((self.palette_image.width + 20, im2.height + 32), "RAG Thresh: {}".format(self.ADJACENT_REGION_DISTANCE_THRESHOLD), fill=(255, 255, 255), font=font)
            d1.text((self.palette_image.width + 20, im2.height + 64), "Superpixel Method: {}".format(self.SUPERPIXEL_METHOD), fill=(255, 255, 255), font=font)
            d1.text((self.palette_image.width + 20, im2.height + 96), "Segments Count: {}".format(self.SEGMENTS_COUNT), fill=(255, 255, 255), font=font)

        for color in palette:
            rgb = color[0]
            rgb = lab2rgb(rgb)
            r = round(rgb[0] * 255)
            g = round(rgb[1] * 255)
            b = round(rgb[2] * 255)

            draw = ImageDraw.Draw(im)
            draw.rectangle([(offset, self.palette_image.height - square_size), (square_size + offset, self.palette_image.height)], fill=(r, g, b))
            draw.text((offset, self.palette_image.height - square_size), "{}".format(color[1]), fill=(255, 255, 255))
            offset += square_size


        trimmed_name = Palette.get_trimmed_image_name(self.image_filepath)
        im.save(os.path.join(self.OUTPUT_DIR, '{0}.png'.format(self.counter)), 'PNG')
        return

        # Write the superpixel result image to file
        if len(self.superpixel_boundary_image) > 0:
            file_path = join('resources/', 'superpixel-' + self.file_name)
            # imsave(file_path, self.superpixel_boundary_image)

        # Either write the palette to an image or superimpose it on top of the above superpixel image
        self.write_palette_to_image(palette)

    """
    # Create a new image that is a line of n number of color squares
    # where the colors match the palette
    # Used primarily for human verification palette testing/verification
    """

    def write_palette_to_image(self, palette):
        trimmed_name = Palette.get_trimmed_image_name(self.image_filepath)

        # print(palette)

        square_size = math.floor(50)
        im = Image.new('RGB', (square_size * len(palette), 50))
        offset = 0
        for color in palette:
            rgb = color[0]
            rgb = lab2rgb(rgb)
            r = round(rgb[0] * 255)
            g = round(rgb[1] * 255)
            b = round(rgb[2] * 255)

            draw = ImageDraw.Draw(im)
            draw.rectangle([(offset, square_size), (square_size + offset, 0)], fill=(r, g, b))
            offset += square_size
        im.save('{0}_palette.png'.format(trimmed_name), 'PNG')
        # self.img.save('resources/palette_images/{0}_palette.png'.format(trimmed_name))
        # self.img.close()

    """
    # Gets the distance between the main_color and all colors in the
    # colors_list. If a color in the list is closer in CIEDE2000
    # than the self.DISTANCE_THRESHOLD, then return that color
    """

    def color_diff(self, main_color, main_score, colors_list, dom_colors):

        for color, score in colors_list.items():
            distance = self.calculate_color_de(main_color, color)
            # self.debug.info('Distance: {0}'.format(distance))
            # if main_color == (11.986346097618384, -10.460822727749647, -1.1409583783878408):
            #     print(distance, color, score, main_score)
            #     quit()
            if distance < self.TANGENTIAL_REGION_DISTANCE_THRESHOLD:
                if dom_colors[main_color] > dom_colors[color]:
                    new_color = main_color
                else:
                    new_color = color


                return [new_color, color]
        return False

    def getHexCode(self, rgb):
        rgb = lab2rgb(rgb)
        r = round(rgb[0] * 255)
        g = round(rgb[1] * 255)
        b = round(rgb[2] * 255)

        shex = '{0:02x}{1:02x}{2:02x}'.format(r, g, b)
        return shex

    def hex_to_lab(self, hex):
        rgb = tuple(int(hex[i:i + 2], 16) / 255 for i in (0, 2, 4))
        lab = rgb2lab(rgb)
        return (lab[0], lab[1], lab[2])

    # Utilities

    @staticmethod
    def get_trimmed_image_name(image_path):

        split_path = image_path.split('/')
        image_name = split_path[len(split_path) - 1]

        trimmed_name = image_name.replace('.png', '').replace('.jpg', '').replace('.jpeg', '')
        return trimmed_name

    @staticmethod
    def sort_dict(dicto):
        return sorted(dicto.items(), key=lambda x: x[1], reverse=True)
