import math
import os, shutil, csv


class CLIError(Exception):

    def __init__(self, value):
        self.value = value


class ParseError(Exception):

    def __init__(self, value):
        self.value = value


class Layer:

    def __init__(self, number, height=0, polyline_velocity=5.0, hatch_velocity=5.0, poly_runcount=1, hatch_runcount=1):
        self.line_number = 0
        self.number = number
        self.height = height
        self.polylines = []
        self.polylinecount = 0
        self.hatches = []
        self.hatchcount = 0
        self.polyline_velocity = polyline_velocity
        self.hatch_velocity = hatch_velocity

        self.poly_runcount = poly_runcount
        self.hatch_runcount = hatch_runcount
        self.polyline_slice_count = 0
        self.hatch_slice_count = 0
        self.poly_time = 0
        self.hatch_time = 0

        self.polyline_beam_current = 5.0
        self.hatch_beam_current = 5.0
        self.polyline_lens_current = 5.0
        self.hatch_lens_current = 5.0
        self.polyline_focus_current = 0.0
        self.hatch_focus_current = 0.0

        self.poly_float_params = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.hatch_float_params = [0.0, 0.0, 0.0, 0.0, 0.0]

    @staticmethod
    def scale_convert(value):
        prev_scale = 250.0
        prev_offset = -125.0
        new_scale = 15400
        new_offset = -7700

        new_value = ((value - prev_offset) * new_scale / prev_scale) + new_offset
        return int(new_value)

    @staticmethod
    def polyline_distance(polyline, polyline_prev):
        return (math.sqrt((polyline[0] - polyline_prev[0]) ** 2 + (polyline[1] - polyline_prev[1]) ** 2))

    @staticmethod
    def hatch_distance(hatch):
        return (math.sqrt((hatch[0] - hatch[2]) ** 2 + (hatch[1] - hatch[3]) ** 2))

    def parse_polyline(self, line):
        start = line.find('/')
        end = line.find(',', start)

        start = end + 1
        end = line.find(',', start)

        start = end + 1
        end = line.find(',', start)
        polylinecount = int(line[start:end])
        if line.count(',') != (polylinecount * 2 + 2):
            print("contour count error, slice : " + str(self.number))
            raise ParseError(1)

        self.polylinecount += polylinecount

        polyline = []
        start = end + 1
        end = line.find(',', start)
        polyline.append(Layer.scale_convert(float(line[start:end])))
        start = end + 1
        end = line.find(',', start)
        polyline.append(Layer.scale_convert(float(line[start:end])))
        polyline.append(0)
        polyline_prev = polyline
        self.polylines.append(polyline)
        for i in range(polylinecount - 2):
            polyline = []
            start = end + 1
            end = line.find(',', start)
            polyline.append(Layer.scale_convert(float(line[start:end])))
            start = end + 1
            end = line.find(',', start)
            polyline.append(Layer.scale_convert(float(line[start:end])))
            time = int(Layer.polyline_distance(polyline, polyline_prev) * self.polyline_velocity)
            polyline.append(time)
            self.poly_time += time
            polyline_prev = polyline
            if polyline[2] > 0:
                self.polylines.append(polyline)
        polyline = []
        start = end + 1
        end = line.find(',', start)
        polyline.append(Layer.scale_convert(float(line[start:end])))
        start = end + 1
        end = line.find('\n', start)
        polyline.append(Layer.scale_convert(float(line[start:end])))
        time = int(Layer.polyline_distance(polyline, polyline_prev) * self.polyline_velocity)
        polyline.append(time)
        self.poly_time += time
        if polyline[2] > 0:
            self.polylines.append(polyline)

    def parse_hatches(self, line):
        start = line.find('/')
        end = line.find(',', start)

        start = end + 1
        end = line.find(',', start)
        hatchcount = int(line[start:end])
        if line.count(',') != (hatchcount * 4 + 1):
            print("hatch count error, slice : " + str(self.number))
            raise ParseError(2)

        self.hatchcount += hatchcount

        for i in range(hatchcount - 1):
            hatch = []
            start = end + 1
            end = line.find(',', start)
            hatch.append(Layer.scale_convert(float(line[start:end])))
            start = end + 1
            end = line.find(',', start)
            hatch.append(Layer.scale_convert(float(line[start:end])))
            start = end + 1
            end = line.find(',', start)
            hatch.append(Layer.scale_convert(float(line[start:end])))
            start = end + 1
            end = line.find(',', start)
            hatch.append(Layer.scale_convert(float(line[start:end])))
            time = int(Layer.hatch_distance(hatch) * self.hatch_velocity)
            hatch.append(time)
            self.hatch_time += time
            self.hatches.append(hatch)
        hatch = []
        start = end + 1
        end = line.find(',', start)
        hatch.append(Layer.scale_convert(float(line[start:end])))
        start = end + 1
        end = line.find(',', start)
        hatch.append(Layer.scale_convert(float(line[start:end])))
        start = end + 1
        end = line.find(',', start)
        hatch.append(Layer.scale_convert(float(line[start:end])))
        start = end + 1
        end = line.find('\n', start)
        hatch.append(Layer.scale_convert(float(line[start:end])))
        time = int(Layer.hatch_distance(hatch) * self.hatch_velocity)
        hatch.append(time)
        self.hatch_time += time
        self.hatches.append(hatch)

    def write_polylines(self, path, count):
        contents = ''
        time = 0

        try:
            zeros = '0' * (3 - len(str(count)))
            file1 = open(path + "/pattern" + str(count) + ".txt", "w")
        except IOError:
            print("File access error")
            raise IOError

        for polyline in self.polylines:
            if (time + polyline[2] > 4000000):
                contents = str(self.number) + "_pattern" + str(count) + ", contour" + "\r\n" + str(
                    time) + "\r\n" + contents[0:len(contents) - 2]
                file1.write(contents)
                file1.close()
                count += 1
                contents = ''
                time = 0
                try:
                    zeros = '0' * (3 - len(str(count)))
                    file1 = open(path + "/pattern" + str(count) + ".txt", "w")
                except IOError:
                    print("File access error")
                    raise IOError

            time += polyline[2]
            contents += str(polyline[2]) + "," + str(polyline[0]) + "," + str(polyline[1]) + "\r\n"

        contents = str(self.number) + "_pattern" + str(count) + ", contour" + "\r\n" + str(time) + "\r\n" + contents[
                                                                                                            0:len(
                                                                                                                contents) - 2]
        file1.write(contents)
        file1.close()
        return count + 1

    def write_hatches(self, path, count):
        contents = ''
        time = 0

        try:
            zeros = '0' * (3 - len(str(count)))
            file1 = open(path + "/pattern" + str(count) + ".txt", "w")
        except IOError:
            print("File access error")
            raise IOError

        for hatch in self.hatches:
            if (time + hatch[4] > 4000000):
                contents = str(self.number) + "_pattern" + str(count) + ", hatch" + "\r\n" + str(
                    time) + "\r\n" + contents[0:len(contents) - 2]
                file1.write(contents)
                file1.close()
                count += 1
                contents = ''
                time = 0
                try:
                    zeros = '0' * (3 - len(str(count)))
                    file1 = open(path + "/pattern" + str(count) + ".txt", "w")
                except IOError:
                    print("File access error")
                    raise IOError

            time += hatch[4]
            contents += "0," + str(hatch[0]) + "," + str(hatch[1]) + "\r\n"
            contents += str(hatch[4]) + "," + str(hatch[2]) + "," + str(hatch[3]) + "\r\n"

        contents = str(self.number) + "_pattern" + str(count) + ", hatch" + "\r\n" + str(time) + "\r\n" + contents[
                                                                                                          0:len(
                                                                                                              contents) - 2]
        file1.write(contents)
        file1.close()
        return count + 1

    def write_layer(self, path, start_count=0):
        try:
            os.mkdir(path)
        except OSError as error:
            raise OSError

        count = start_count

        if (self.polylinecount):
            count = self.write_polylines(path, count)
            self.polyline_slice_count = count - start_count

        if (self.hatchcount):
            count = self.write_hatches(path, count)
            self.hatch_slice_count = count - self.polyline_slice_count - start_count


class Preheat:

    def __init__(self):
        self.hatch_length = 4620  # 150 mm box
        self.hatch_distance = 0.1
        self.hatch_distance_count = 0
        self.hatchcount = 0
        self.polylinecount = 0
        self.hatches = []
        self.hatch_velocity = 0.05
        self.hatch_runcount = 1
        self.time = 0

        self.hatch_beam_current = 1.0
        self.hatch_lens_current = 494.0
        self.hatch_focus_current = 494.0

        self.hatch_float_params = [0.0, 0.0, 0.0, 0.0, 0.0]

        self.generate_hatches()

    def generate_hatches(self):
        hatch_distance_count = int(self.hatch_distance * 1540 / 25.0)
        self.hatches = []
        self.hatchcount = 0
        self.time = 0
        x = -self.hatch_length
        time = int(self.hatch_length * 2 * self.hatch_velocity)

        while (x < self.hatch_length):
            self.hatches.append([x, self.hatch_length, x, -self.hatch_length, time])
            x += hatch_distance_count
            self.hatchcount += 1
            self.time += time

    def modify_pattern(self, hatch_velocity, hatch_distance, hatch_runcount, hatch_beam_current=5.0, \
                       hatch_lens_current=5.0, hatch_focus_current=0.0):

        self.hatch_runcount = hatch_runcount

        self.hatch_beam_current = hatch_beam_current
        self.hatch_lens_current = hatch_lens_current
        self.hatch_focus_current = hatch_focus_current

        change_flag = False
        if (self.hatch_velocity != hatch_velocity):
            self.hatch_velocity = hatch_velocity
            change_flag = True

        if (self.hatch_distance != hatch_distance):
            self.hatch_distance = hatch_distance
            change_flag = True

        if (change_flag):
            self.generate_hatches()

    def write_pattern(self, path, count=0, layer=0):
        if (os.path.isdir(path) == 0):
            try:
                os.mkdir(path)
            except OSError:
                raise OSError

        contents = ''
        time = 0

        try:
            zeros = '0' * (3 - len(str(count)))
            file1 = open(path + "/pattern" + str(count) + ".txt", "w")
        except IOError:
            print("File access error")
            raise IOError

        for hatch in self.hatches:
            time += hatch[4]
            contents += "0," + str(hatch[0]) + "," + str(hatch[1]) + "\r\n"
            contents += str(hatch[4]) + "," + str(hatch[2]) + "," + str(hatch[3]) + "\r\n"

        contents = str(layer) + "_pattern" + str(count) + ", preheat" + "\r\n" + str(time) + "\r\n" + contents[0:len(
            contents) - 2]
        file1.write(contents)
        file1.close()
        return count + 1


class CLIFile:

    def __init__(self, path):

        try:
            file1 = open(path, "r")
        except IOError:
            print("File read error")
            raise IOError

        self.lines = file1.readlines()
        file1.close()

        flag = 0

        if (self.lines[0] != "$$HEADERSTART\n"):
            flag = 1
        elif (self.lines[1] != "$$ASCII\n"):
            flag = 2
        elif (self.lines[3] != "$$VERSION/200\n"):
            flag = 3

        if (flag):
            raise CLIError(flag)

        self.version = 200
        self.date = ""
        self.layers = []
        self.layercount = 0
        self.preheat_bottom = []
        self.preheat_layers = []
        self.preheat_bottom_count = 0
        self.preheat_layers_count = 0

    def count_layers(self):

        for line in self.lines:
            if (line == "$$GEOMETRYSTART\n"):
                raise CLIError(4)

            if ("$$DATE/" in line):
                self.date = line[len("$$DATE/"):]
                self.date = self.date[0:2] + '/' + self.date[2:4] + '/' + self.date[4:]

            if ("$$LAYERS/" in line):
                self.layercount = int(line[len("$$LAYERS/"):])
                break

        for i in range(self.layercount):
            self.layers.append(Layer(i))

    def parse_layer(self, index):

        m = self.layers[index].line_number
        line = self.lines[m]
        start = line.find('/') + 1
        end = line.find('\n')
        self.layers[index].height = round(float(line[start:end]), 1)
        self.layers[index].polylines = []
        self.layers[index].polylinecount = 0
        self.layers[index].hatches = []
        self.layers[index].hatchcount = 0
        self.layers[index].poly_time = 0
        self.layers[index].hatch_time = 0

        while (1):
            m += 1
            line = self.lines[m]

            if (line == "$\n"):
                continue

            elif ("$HATCHES/" in line):
                try:
                    self.layers[index].parse_hatches(line)
                except ParseError as error:
                    print("Hatch parse error in line " + str(m))
                    raise ParseError(error.value)

            elif ("$POLYLINE/" in line):
                try:
                    self.layers[index].parse_polyline(line)
                except ParseError as error:
                    print("Polyline parse error in line " + str(m))
                    raise ParseError(error.value)

            elif ("$$LAYER/" in line) or ("$$GEOMETRYEND" in line):
                break

        return m

    def setlayer_parameters(self, index, polyline_velocity, hatch_velocity, poly_runcount, hatch_runcount,
                            polyline_beam_current=5.0, \
                            hatch_beam_current=5.0, polyline_lens_current=5.0, hatch_lens_current=5.0,
                            polyline_focus_current=0.0, hatch_focus_current=0.0):

        self.layers[index].poly_runcount = poly_runcount
        self.layers[index].hatch_runcount = hatch_runcount

        self.layers[index].polyline_beam_current = polyline_beam_current
        self.layers[index].hatch_beam_current = hatch_beam_current
        self.layers[index].polyline_lens_current = polyline_lens_current
        self.layers[index].hatch_lens_current = hatch_lens_current
        self.layers[index].polyline_focus_current = polyline_focus_current
        self.layers[index].hatch_focus_current = hatch_focus_current

        change_velocity_flag = False
        if (self.layers[index].polyline_velocity != polyline_velocity):
            self.layers[index].polyline_velocity = polyline_velocity
            change_velocity_flag = True

        if (self.layers[index].hatch_velocity != hatch_velocity):
            self.layers[index].hatch_velocity = hatch_velocity
            change_velocity_flag = True

        if (change_velocity_flag):
            self.parse_layer(index)

    def parse_layers(self, lines_complete):

        s = 0
        for line in self.lines:
            if (line == "$$GEOMETRYSTART\n"):
                break
            else:
                s += 1

        m = s + 1
        for i in range(self.layercount):
            line = self.lines[m]

            if ("$$LAYER/" in line):
                self.layers[i].height = float(line[len("$$LAYER/"):])
                self.layers[i].line_number = m

            else:
                break

            try:
                m = self.parse_layer(i)
            except ParseError as error:
                print("Error in layer " + str(i))
                raise ParseError(error.value)

            lines_complete.value = int(100 * m / len(self.lines))

    def write_csv(self, path):

        content = []
        content.append(
            ["slice", "pattern", "Runs", "Beam current", "Lens current", "Focus current", "Parameter 4", "Parameter 5",
             "Parameter 6", \
             "Parameter 7", "Parameter 8"])

        # content.append([0])
        i = 0
        flag = 0

        if self.preheat_bottom_count:
            for preheat_layer in self.preheat_bottom:
                content.append([0, i, preheat_layer.hatch_runcount, preheat_layer.hatch_beam_current,
                                preheat_layer.hatch_lens_current, \
                                preheat_layer.hatch_focus_current, preheat_layer.hatch_float_params[0],
                                preheat_layer.hatch_float_params[1], \
                                preheat_layer.hatch_float_params[2], preheat_layer.hatch_float_params[3],
                                preheat_layer.hatch_float_params[4]])
                i += 1

            content.append([])
            flag = 1

        i = 0
        for layer in self.layers:
            # content.append([layer.number + 1])

            for preheat_layer in self.preheat_layers:
                content.append([layer.number + flag, i, preheat_layer.hatch_runcount, preheat_layer.hatch_beam_current,
                                preheat_layer.hatch_lens_current, \
                                preheat_layer.hatch_focus_current, preheat_layer.hatch_float_params[0],
                                preheat_layer.hatch_float_params[1], \
                                preheat_layer.hatch_float_params[2], preheat_layer.hatch_float_params[3],
                                preheat_layer.hatch_float_params[4]])
                i += 1

            for _ in range(layer.polyline_slice_count):
                content.append([layer.number + flag, i, layer.poly_runcount, layer.polyline_beam_current,
                                layer.polyline_lens_current, \
                                layer.polyline_focus_current, layer.poly_float_params[0], layer.poly_float_params[1],
                                layer.poly_float_params[2], \
                                layer.poly_float_params[3], layer.poly_float_params[4]])
                i += 1

            for _ in range(layer.hatch_slice_count):
                content.append(
                    [layer.number + flag, i, layer.hatch_runcount, layer.hatch_beam_current, layer.hatch_lens_current, \
                     layer.hatch_focus_current, layer.hatch_float_params[0], layer.hatch_float_params[1],
                     layer.hatch_float_params[2] \
                        , layer.hatch_float_params[3], layer.hatch_float_params[4]])
                i += 1

            content.append([])
            i = 0

        if (os.path.isdir(path)):
            with open(path + '/Parameter.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(content)
            return 1
        else:
            print("not a directory")
            return 0

    def write_layers(self, path, layers_saved, pattern_start_number=0):

        try:
            shutil.rmtree(path)
        except OSError:
            pass

        try:
            os.mkdir(path)
        except OSError as error:
            print("error making directory")
            raise OSError

        preheat_bottom_count = 0
        layer_start_number = 0
        for preheat_layer in self.preheat_bottom:
            preheat_bottom_count = preheat_layer.write_pattern(path + "/slice0", preheat_bottom_count)
            layer_start_number = 1

        for layer in self.layers:
            zeros = '0' * (3 - len(str(layer.number + layer_start_number)))
            layer.write_layer(path + "/slice" + str(layer.number + layer_start_number), pattern_start_number)

            preheat_layer_count = 0
            for preheat_layer in self.preheat_layers:
                zeros = '0' * (3 - len(str(layer.number + layer_start_number)))
                preheat_layer_count = preheat_layer.write_pattern(
                    path + "/slice" + str(layer.number + layer_start_number), \
                    preheat_layer_count, layer.number)

            layers_saved.value = int(100 * layer.number / self.layercount)

        self.write_csv(path)


class Parameterfile:

    def __init__(self, param_count=20, beam_current=5.0, lens_current=5.0, focus_current=5.0, parameter4=0.0,
                 parameter5=0.0):

        self.parameters = []
        self.parameters.append(["Beam current", "Lens current", "Focus current", "Parameter 4", "Parameter 5"])
        for _ in range(param_count):
            self.parameters.append([beam_current, lens_current, focus_current, parameter4, parameter5])

    def change_parameters(self, index, beam_current, lens_current, focus_current, parameter4, parameter5):

        self.parameters[index + 1] = [beam_current, lens_current, focus_current, parameter4, parameter5]

    def write_parameters(self, path):

        if (os.path.isdir(path)):
            if (os.path.isfile(path + 'Parameter.csv')):
                os.remove(path + 'Parameter.csv')
            with open(path + 'Parameter.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(self.parameters)
            return 1
        else:
            print("not a directory")
            return 0


class Crosscalibrate:

    def __init__(self, hatch_factor=10, hatch_velocity=0.1):

        self.hatch_factor = hatch_factor
        self.hatch_velocity = hatch_velocity
        self.hatches = []
        self.hatchcount = 0
        self.polylinecount = 0
        self.hatch_runcount = 1
        self.time = 0

        self.hatch_beam_current = 5.0
        self.hatch_lens_current = 5.0
        self.hatch_focus_current = 0.0

        self.hatch_float_params = [0.0, 0.0, 0.0, 0.0, 0.0]

        self.generate_hatches()

    @staticmethod
    def distance_count(x1, y1, x2, y2):
        return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))

    def generate_hatches(self):
        hatch_distance_count = int(15400 / self.hatch_factor)
        self.hatches = []
        self.hatchcount = 0
        self.time = 0

        x = -7700
        time = int(15400 * self.hatch_velocity)

        while (x <= 7700):
            self.hatches.append([x, 7700, x, -7700, time])
            x += hatch_distance_count
            self.hatchcount += 1
            self.time += time

        y = -7700

        while (y <= 7700):
            self.hatches.append([7700, y, -7700, y, time])
            y += hatch_distance_count
            self.hatchcount += 1
            self.time += time

        x = hatch_distance_count - 7700
        y = hatch_distance_count - 7700

        while (x <= 7700):
            time = int(self.hatch_velocity * self.distance_count(-7700, y, x, -7700))
            self.hatches.append([-7700, y, x, -7700, time])
            x += hatch_distance_count
            y += hatch_distance_count
            self.hatchcount += 1
            self.time += time

        x = hatch_distance_count - 7700
        y = hatch_distance_count - 7700

        while (x < 7700):
            time = int(self.hatch_velocity * self.distance_count(x, 7700, 7700, y))
            self.hatches.append([x, 7700, 7700, y, time])
            x += hatch_distance_count
            y += hatch_distance_count
            self.hatchcount += 1
            self.time += time

        x = hatch_distance_count - 7700
        y = 7700 - hatch_distance_count

        while (x <= 7700):
            time = int(self.hatch_velocity * self.distance_count(-7700, y, x, 7700))
            self.hatches.append([-7700, y, x, 7700, time])
            x += hatch_distance_count
            y -= hatch_distance_count
            self.hatchcount += 1
            self.time += time

        x = hatch_distance_count - 7700
        y = 7700 - hatch_distance_count

        while (x < 7700):
            time = int(self.hatch_velocity * self.distance_count(x, -7700, 7700, y))
            self.hatches.append([x, -7700, 7700, y, time])
            x += hatch_distance_count
            y -= hatch_distance_count
            self.hatchcount += 1
            self.time += time

    def write_pattern(self, path, count=0):
        if (os.path.isdir(path) == 0):
            try:
                os.mkdir(path)
            except OSError:
                raise OSError

        contents = ''
        time = 0

        try:
            zeros = '0' * (3 - len(str(count)))
            file1 = open(path + "/pattern" + str(count) + ".txt", "w")
        except IOError:
            print("File access error")
            raise IOError

        for hatch in self.hatches:
            time += hatch[4]
            contents += "0," + str(hatch[0]) + "," + str(hatch[1]) + "\r\n"
            contents += str(hatch[4]) + "," + str(hatch[2]) + "," + str(hatch[3]) + "\r\n"

        contents = "0_pattern" + str(count) + ", crosscalibrate" + "\r\n" + str(time) + "\r\n" + contents[
                                                                                                 0:len(contents) - 2]
        file1.write(contents)
        file1.close()
        return count + 1


class Squarecalibrate:

    def __init__(self, poly_distance=25, dot_spacing=5):

        self.poly_distance = poly_distance
        self.dot_spacing = dot_spacing
        self.polylines = []
        self.hatchcount = 0
        self.polylinecount = 0
        self.poly_runcount = 1
        self.time = 0

        self.polyline_beam_current = 5.0
        self.polyline_lens_current = 5.0
        self.polyline_focus_current = 0.0

        self.polyline_float_params = [0.0, 0.0, 0.0, 0.0, 0.0]

        self.generate_polylines()

    def generate_polylines(self):
        self.polylines = []
        self.polylinecount = 0
        self.time = 0
        poly_distance_count = int(self.poly_distance * 1540 / 25.0)
        dot_spacing_count = int(self.dot_spacing * 1540 / 25.0)
        x = poly_distance_count

        while (x <= 7700):
            time = int(2 * x / dot_spacing_count)
            self.polylines.append([x, x, 0])
            self.polylines.append([-1 * x, x, time])
            self.polylines.append([-1 * x, -1 * x, time])
            self.polylines.append([x, -1 * x, time])
            self.polylines.append([x, x, time])
            self.time += 4 * time
            self.polylinecount += 5
            x += poly_distance_count

    def write_pattern(self, path, count=0):
        if (os.path.isdir(path) == 0):
            try:
                os.mkdir(path)
            except OSError:
                raise OSError

        contents = ''
        time = 0

        try:
            zeros = '0' * (3 - len(str(count)))
            file1 = open(path + "/pattern" + str(count) + ".txt", "w")
        except IOError:
            print("File access error")
            raise IOError

        for polyline in self.polylines:
            time += polyline[2]
            contents += str(polyline[2]) + "," + str(polyline[0]) + "," + str(polyline[1]) + "\r\n"

        contents = "0_pattern" + str(count) + ", squarecalibrate" + "\r\n" + str(time) + "\r\n" + contents[
                                                                                                  0:len(contents) - 2]
        file1.write(contents)
        file1.close()
        return count + 1


class Dotcalibrate:

    def __init__(self, hatch_distance=25, dot_spacing=5, dot_time=100):

        self.hatch_distance = hatch_distance
        self.dot_spacing = dot_spacing
        self.dot_time = dot_time

        self.hatches = []
        self.hatchcount = 0
        self.polylinecount = 0
        self.hatch_runcount = 1
        self.time = 0

        self.hatch_beam_current = 5.0
        self.hatch_lens_current = 5.0
        self.hatch_focus_current = 0.0

        self.hatch_float_params = [0.0, 0.0, 0.0, 0.0, 0.0]

        self.generate_hatches()

    def generate_hatches(self):
        self.hatches = []
        self.hatchcount = 0
        self.time = 0
        hatch_distance_count = int(self.hatch_distance * 1540 / 25.0)
        dot_spacing_count = int(self.dot_spacing * 1540 / 25.0)
        x = hatch_distance_count

        while (x <= 7700):
            t = 0
            while (t < 2 * x):
                self.hatches.append([x, x - t, x, x - t, self.dot_time])
                t += dot_spacing_count
                self.hatchcount += 1
                self.time += self.dot_time

            t = 0
            while (t < 2 * x):
                self.hatches.append([x - t, -1 * x, x - t, -1 * x, self.dot_time])
                t += dot_spacing_count
                self.hatchcount += 1
                self.time += self.dot_time

            t = 0
            while (t < 2 * x):
                self.hatches.append([-1 * x, t - x, -1 * x, t - x, self.dot_time])
                t += dot_spacing_count
                self.hatchcount += 1
                self.time += self.dot_time

            t = 0
            while (t < 2 * x):
                self.hatches.append([t - x, x, t - x, x, self.dot_time])
                t += dot_spacing_count
                self.hatchcount += 1
                self.time += self.dot_time

            x += hatch_distance_count

    def write_pattern(self, path, count=0):
        if (os.path.isdir(path) == 0):
            try:
                os.mkdir(path)
            except OSError:
                raise OSError

        contents = ''
        time = 0

        try:
            zeros = '0' * (3 - len(str(count)))
            file1 = open(path + "/pattern" + str(count) + ".txt", "w")
        except IOError:
            print("File access error")
            raise IOError

        for hatch in self.hatches:
            time += hatch[4]
            contents += "0," + str(hatch[0]) + "," + str(hatch[1]) + "\r\n"
            contents += str(hatch[4]) + "," + str(hatch[2]) + "," + str(hatch[3]) + "\r\n"

        contents = "0_pattern" + str(count) + ", dotcalibrate" + "\r\n" + str(time) + "\r\n" + contents[
                                                                                               0:len(contents) - 2]
        file1.write(contents)
        file1.close()
        return count + 1


class Numbercalibrate:

    def __init__(self, height=1400, width=350, start_x=-7600, start_y=7600, velocity=0.54, letters=5):

        self.start_x = start_x
        self.start_y = start_y
        self.letters = letters
        self.height = height
        self.width = width
        self.velocity = velocity
        self.demark = []

        self.hatches = []
        self.hatchcount = 0
        self.polylinecount = 0
        self.hatch_runcount = 1
        self.time = 0

        self.hatch_beam_current = 5.0
        self.hatch_lens_current = 5.0
        self.hatch_focus_current = 0.0
        self.hatch_float_params = [0.0, 0.0, 0.0, 0.0, 0.0]

        self.generate_hatches()

    def generate_hatches(self):
        self.hatches = []
        self.hatchcount = 0
        self.time = 0

        self.demark.append(0)
        if (self.letters > 0):
            x = 0
            time = int(self.height * self.velocity)
            while (x < self.width):
                self.hatches.append(
                    [self.start_x + x, self.start_y, self.start_x + x, self.start_y - self.height, time])
                self.hatchcount += 1
                self.time += time
                x += 20
            self.demark.append(self.hatchcount)

        if (self.letters > 1):
            x = 0
            time = int(self.height * self.velocity)
            while (x < self.width):
                self.hatches.append(
                    [self.start_x + 1000 + x, self.start_y, self.start_x + 1000 + x, self.start_y - self.height, time])
                self.hatchcount += 1
                self.time += time
                x += 20

            x = 0
            time = int(self.height * self.velocity)
            while (x < self.width):
                self.hatches.append(
                    [self.start_x + 1500 + x, self.start_y, self.start_x + 1500 + x, self.start_y - self.height, time])
                self.hatchcount += 1
                self.time += time
                x += 20
            self.demark.append(self.hatchcount)

        if (self.letters > 2):
            x = 0
            time = int(self.height * self.velocity)
            while (x < self.width):
                self.hatches.append(
                    [self.start_x + 2500 + x, self.start_y, self.start_x + 2500 + x, self.start_y - self.height, time])
                self.hatchcount += 1
                self.time += time
                x += 20

            x = 0
            time = int(self.height * self.velocity)
            while (x < self.width):
                self.hatches.append(
                    [self.start_x + 3000 + x, self.start_y, self.start_x + 3000 + x, self.start_y - self.height, time])
                self.hatchcount += 1
                self.time += time
                x += 20

            x = 0
            time = int(self.height * self.velocity)
            while (x < self.width):
                self.hatches.append(
                    [self.start_x + 3500 + x, self.start_y, self.start_x + 3500 + x, self.start_y - self.height, time])
                self.hatchcount += 1
                self.time += time
                x += 20
            self.demark.append(self.hatchcount)

        if (self.letters > 3):
            x = 0
            time = int(self.height * self.velocity)
            while (x < self.width):
                self.hatches.append(
                    [self.start_x + 4500 + x, self.start_y, self.start_x + 4500 + x, self.start_y - self.height, time])
                self.hatchcount += 1
                self.time += time
                x += 20

            x = 0
            time = int(self.height * self.velocity)
            while (x < self.width):
                self.hatches.append(
                    [self.start_x + 5000 + x, self.start_y, self.start_x + 5500 + x, self.start_y - self.height, time])
                self.hatchcount += 1
                self.time += time
                x += 20

            x = 0
            time = int(self.height * self.velocity)
            while (x < self.width):
                self.hatches.append(
                    [self.start_x + 6000 + x, self.start_y, self.start_x + 5500 + x, self.start_y - self.height, time])
                self.hatchcount += 1
                self.time += time
                x += 20
            self.demark.append(self.hatchcount)

        if (self.letters > 4):
            x = 0
            time = int(self.height * self.velocity)
            while (x < self.width):
                self.hatches.append(
                    [self.start_x + 7000 + x, self.start_y, self.start_x + 7500 + x, self.start_y - self.height, time])
                self.hatchcount += 1
                self.time += time
                x += 20

            x = 0
            time = int(self.height * self.velocity)
            while (x < self.width):
                self.hatches.append(
                    [self.start_x + 8000 + x, self.start_y, self.start_x + 7500 + x, self.start_y - self.height, time])
                self.hatchcount += 1
                self.time += time
                x += 20
            self.demark.append(self.hatchcount)

    def write_pattern(self, path, count=0):
        if (os.path.isdir(path) == 0):
            try:
                os.mkdir(path)
            except OSError:
                raise OSError

        print(self.demark)

        for i in range(self.letters):
            contents = ''
            time = 0

            try:
                zeros = '0' * (3 - len(str(count)))
                file1 = open(path + "/pattern" + str(count) + ".txt", "w")
            except IOError:
                print("File access error")
                raise IOError

            for hatch in self.hatches[self.demark[i]: self.demark[i + 1]]:
                time += hatch[4]
                contents += "0," + str(hatch[0]) + "," + str(hatch[1]) + "\r\n"
                contents += str(hatch[4]) + "," + str(hatch[2]) + "," + str(hatch[3]) + "\r\n"

            contents = "0_pattern" + str(count) + ", numbercalibrate" + "\r\n" + str(time) + "\r\n" + contents[0:len(
                contents) - 2]
            file1.write(contents)
            file1.close()
            count += 1

        return count + 1


if __name__ == "__main__":

    print("main:")

    params = Parameterfile()

    for i in range(20):
        print(params.parameters[i])

    """params.write_parameters('./')

	try:
		#clif ile = CLif ile("/home/j2002/Desktop/Cylinder.cli")
		#clif ile = CLif ile("../CLI Sahil/cylinder hollow/cylinder hollow.cli")
		#clif ile = CLif ile("/home/sahil/Documents/M3DP/CLI Sahil/IISC logo/IISC logo.cli")
		#clif ile = CLif ile("../CLI Sahil/Cylinder cli/cylinder with 25 island.cli")
		#clif ile = CLif ile("../CLI Sahil/Cylinder cli/cylinder with 100 island.cli", 0.541, 0.541) 
		#clif ile = CLif ile("../CLI Sahil/Cuboid/cuboid cli info.cli")
		#clif ile = CLif ile("../CLI Sahil/Cuboid/cuboid with 100 island.cli")
		#clif ile = CLif ile("../CLI Sahil/Cylinder small hatch/2mm thick slice.cli")
		#clif ile = CLif ile("../CLI Sahil/Cylinder small hatch/2mm thick with 5mm distance.cli", 16.233, 16.233) # 1 m/s beam velocity

	except IOError:
		print("Error opening cli file")
		exit()
	except CLIError as error:
		print("File format error: ", error.value)
		exit()

	try:
		clif ile.count_layers()
		print(clif ile.layercount)
	except CLIError as error:
		print("Layer count not found")
	except ParseError as error:
		print("Parse error")

	try:
		clif ile.parse_layers()
	except ParseError as error:
		print("Parse error")

	#clif ile.write_layers("../CLI Sahil/1mm layer thickness/clif older")
	#clif ile.write_layers("../CLI Sahil/cylinder hollow/clif older")
	#clif ile.write_layers("../CLI Sahil/IISC logo/clif older")
	#clif ile.write_layers("../CLI Sahil/Cylinder cli/clif older 25 islands")
	#clif ile.write_layers("../CLI Sahil/Cylinder cli/clif older 100 islands")
	#clif ile.write_layers("../CLI Sahil/Cuboid/clif older info")
	#clif ile.write_layers("../CLI Sahil/Cuboid/clif older 100 island")
	#clif ile.write_layers("../CLI Sahil/Cylinder small hatch/clif older thick slice")
	#clif ile.write_layers("../CLI Sahil/Cylinder small hatch/clif older 5mm slice")"""
