"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 2/27/2024

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Reference:

"""
from __future__ import annotations

from typing import Generator
from typing import List
from typing import TYPE_CHECKING
from typing import Union

import matplotlib.pyplot as plt
import numpy as np
from IPython.display import HTML
from IPython.display import Image
from matplotlib.animation import FuncAnimation

if TYPE_CHECKING:
    from common import Shape
    from common import GridLike


class GridRecordable(list):
    """
    A Grid that records itself as a matrix in a list when the value of a cell or position changes.
    """
    shape: Shape
    bool_should_record: bool
    _grid_recordable_parent: Union[GridRecordable, None]
    list_matrix_copy: List[np.ndarray]

    def __init__(self,
                 shape: Shape,
                 value_in_cell: Union[None, int] = 0,
                 bool_should_record: bool = False,
                 _grid_recordable_parent: Union[GridRecordable, None] = None,

                 ):
        super().__init__()

        self.shape = shape
        self.bool_should_record = bool_should_record
        self._grid_recordable_parent = _grid_recordable_parent

        self.list_matrix_copy = []

        if _grid_recordable_parent is None:
            self._grid_recordable_parent = self

        if len(shape) > 1:
            for index_row in range(self.shape[0]):
                self.append(
                    GridRecordable(
                        tuple(shape[1:]),
                        value_in_cell,
                        False,
                        _grid_recordable_parent=self
                    )
                )
        else:
            super().__init__((value_in_cell for index in range(shape[0])))
            self.bool_should_record = True

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        if self.bool_should_record:
            self._grid_recordable_parent._record_self_to_list_matrix_recorded()

    def _record_self_to_list_matrix_recorded(self):
        matrix = np.array(self)
        self.list_matrix_copy.append(matrix)

    def get_list_matrix_recorded(self) -> List[np.ndarray]:
        return self.list_matrix_copy


"""
The below was me making a object that contains a callback where solutions to make the spiral
would call the callback and the callback would copy the grid, the list or sequence of grids at
differnt times of the algorithm would then be used to create a gif or animation and would
be displayed in jupyter
"""

# from __future__ import annotations
#
# from typing import Generator
# from typing import List
# from typing import TYPE_CHECKING
# from typing import Union
#
# import matplotlib.pyplot as plt
# import numpy as np
# from IPython.display import HTML
# from IPython.display import Image
# from matplotlib.animation import FuncAnimation
#
# if TYPE_CHECKING:
#     from common import Shape
#     from common import GridLike
#
# class ContainerMatrix():
#     path_abs_filename: str
#     path_directory: str
#     list_matrix: List[np.ndarray]
#
#     def __init__(self,
#                  # filename: str,
#                  # path_directory:
#                  # str ="./media"
#                  ):
#         # self.path_abs_filename = filename
#         # self.path_directory = path_directory
#         self.list_matrix = []
#
#         ####
#
#         self.animation: Union[FuncAnimation, None] = None
#
#     def callback_grid_like(self, grid_like: GridLike) -> None:
#         self.list_matrix.append(np.array(grid_like))
#
#     def create_animation(self) -> None:
#
#         def generator_pull_from_list() -> Generator[np.ndarray, None, None]:
#             for matrix in self.list_matrix:
#                 yield matrix
#
#         generator_matrix = generator_pull_from_list()
#
#         # Create a figure and axes
#         figure, axes = plt.subplots()
#
#         # Function to update the plot for each frame
#         def update(frame):
#             axes.clear()
#
#             matrix = next(generator_matrix)
#
#             # Display the numbers in the matrix
#             for i in range(matrix.shape[0]):
#                 for j in range(matrix.shape[1]):
#                     axes.text(j, i, f'{matrix[i, j]:.2f}', ha='center', va='center', color='white')
#
#             axes.imshow(matrix, cmap='viridis')
#             axes.set_title(f"Frame {frame}")
#
#         # Create the animation
#         self.animation = FuncAnimation(figure, update, frames=len(self.list_matrix), interval=100)
#
#     # def _get_path_(self):
#     #     pass
#     #
#     # def save_to_gif(self):
#     #     # Save the animation as a GIF
#     #     self.animation.save(f'{seFF NAME}.gif')
#     #
#     def display_as_gif(self):
#         Image(url='example.gif')
#
#     def display_as_html(self) -> None:
#         HTML(self.animation.to_jshtml())

"""
Useful code that you should put into a jupyter cell
"""

# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
#
# # Create a figure and axes
# fig, ax = plt.subplots()
#
#
# # Function to update the plot for each frame
# def update(frame):
#     ax.clear()
#     matrix = generate_matrix(frame)  # Replace with your function to generate the matrix for each frame
#
#     # Display the numbers in the matrix
#     for i in range(matrix.shape[0]):
#         for j in range(matrix.shape[1]):
#             ax.text(j, i, f'{matrix[i, j]:.2f}', ha='center', va='center', color='white')
#
#     ax.matshow(matrix, cmap='viridis')
#     ax.set_title(f"Frame {frame}")
#
#
# # Function to generate a matrix for each frame (replace this with your own logic)
# def generate_matrix(frame):
#     # Example: A matrix that changes with time
#     return np.random.rand(5, 5) * (frame + 1)
#
#
# # Set the number of frames (adjust as needed)
# # num_frames = 625
# num_frames = 10
#
# # Create the animation
# animation = FuncAnimation(fig,
#                           update,
#                           frames=num_frames,
#                           #   interval=500,
#                           )
#
# # Save the animation as a GIF
# # animation.save('matrix_animation.gif')
#
# # Close the figure created above because you only care about the animation
# plt.close(figure)
#
# from IPython.display import HTML
#
# HTML(animation.to_jshtml())  # Only works in a juptyer cell on the global level and not in a code's body
