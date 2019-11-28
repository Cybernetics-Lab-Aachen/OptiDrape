import numpy as np


class ScoreCalculator(object):
    def __init__(self, fixed_x_size, fixed_y_size, weight_max_angle, scale=1):
        if not isinstance(fixed_x_size, int):
            raise TypeError("Fixed x size has to be inherited from int")
        else:
            self.fixed_x_size = fixed_x_size

        if not isinstance(fixed_y_size, int):
            raise TypeError("Fixed y size has to be inherited from int")
        else:
            self.fixed_y_size = fixed_y_size

        if 0 > weight_max_angle or 1 < weight_max_angle:
            raise ValueError("The weight of the max angle has to be within [0,1]. weight_max_angle", weight_max_angle)
        else:
            self.weight_max_angle = weight_max_angle

        if not isinstance(scale, (int, float)):
            raise TypeError("Threshold has to be inherited from int or float")
        else:
            self.scale = scale

    def calculate_score(self, input_data, threshold):
        # Check input_data
        if len(input_data.shape) == 2:  # Implicitly points to the fact, that this data has its origin in DrapeFix
            shape = input_data.shape
            if shape[0] != self.fixed_x_size:
                raise ValueError("Fixed x-dimension size is violated. Should be",
                                 self.fixed_x_size,
                                 "instead of",
                                 shape[0])
            elif shape[1] != self.fixed_y_size:
                raise ValueError("Fixed x-dimension size is violated. Should be",
                                 self.fixed_y_size,
                                 "instead of",
                                 shape[1])
            input_data = input_data.flatten()
        elif len(input_data.shape) > 2:
            raise ValueError("Dimension has to be less or equal to 2. Input dimension is", len(input_data.shape))

        # get maximum sheer angle

        max_angle = np.max(np.abs(input_data))


        # get values over a threshold
        values_over_threshold = input_data[input_data >= threshold]

        # get percentage of angles over threshold
        perc_over_threshold = len(values_over_threshold) / len(input_data)

        # scale over threshold values to max_angle
        scaled_values_over_threshold = values_over_threshold / max_angle

        # calculate threshold value
        first_factor = perc_over_threshold + 1
        second_factor = np.sum(scaled_values_over_threshold) * perc_over_threshold + 1

        threshold_value = first_factor * second_factor

        # weighted score
        weighted_score = self.weight_max_angle * max_angle + (1 - self.weight_max_angle) * threshold_value

        # score
        score = self.scale * weighted_score

        return weighted_score


def main():
    sc = ScoreCalculator(20, 20, 1, 0.4)
    a = np.random.rand(20, 20) * 2
    print("Score =",sc.calculate_score(a))
    a = np.random.rand(14) * 2
    print("Score =",sc.calculate_score(a))
    # sc2 = ScoreCalculator(20.,20, 1, 0.4) # Raises exception. That is the correct response

    # a = np.random.rand(14,20) * 2
    # print("Score =",sc.calculate_score(a)) # Raises exception. That is the correct response

    # a = np.random.rand(14,14,14) * 2
    # print("Score =",sc.calculate_score(a)) # Raises exception. That is the correct response


if __name__ == '__main__':
    main()
