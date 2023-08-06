import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import os

from myterial import grey_light, blue_grey_dark, grey, red_dark

from brainrender import Scene, settings
import bgheatmaps as bgh


"""
    This examlpe shows how to combine 3D rendering in brainrender 
    and bgh.get_structures_slice_coords from bgheatmaps to create a
    3D + 2D schematic e.g. for a paper figure
"""

settings.SHOW_AXES = False
settings.ROOT_ALPHA = 0.05
settings.BACKGROUND_COLOR = "white"

# ---------------------------------------------------------------------------- #
#                                 3D rendering                                 #
# ---------------------------------------------------------------------------- #

scene = Scene()

# get some thalamus sub regions
regions = []
all_descendants = scene.atlas.get_structure_descendants("TH")
for region in all_descendants:
    if scene.atlas.get_structure_ancestors(region)[::-1].index("TH") == 2:
        regions.append(region)


# show thalamus
th = scene.add_brain_region("TH", alpha=1, silhouette=True, color=grey)

# add sub regions meshes, coloring LGv and LGd only
regions_actors = []
for region in regions:
    color = red_dark if "LG" in region else grey_light
    regions_actors.append(scene.add_brain_region(region, color=color))


# get a plane to slice thorugh TH subregions
plane_position = th.centerOfMass() + np.array([100, 0, 0])
plane_norm = (1, 0, 0)
plane_size = (6000, 4000)


# slice through sub regions
plane = scene.atlas.get_plane(plane_position, norm=plane_norm)
scene.slice(plane, actors=regions_actors, close_actors=True)
scene.slice(plane, actors=[th], close_actors=False)

# add a second plane for visualization
plane2 = scene.add(
    scene.atlas.get_plane(
        th.centerOfMass() + np.array([80, 0, 0]),
        norm=plane_norm,
        sx=plane_size[0],
        sy=plane_size[1],
        alpha=0.2,
        color=blue_grey_dark,
    )
)
scene.add_silhouette(plane2, lw=4)

# render
camera = {
    "pos": (-14061, -6512, -32987),
    "viewup": (0, -1, 0),
    "clippingRange": (17635, 58635),
    "focalPoint": (7830, 4296, -5694),
    "distance": 36618,
}
scene.render(camera=camera, zoom=1.75, interactive=False)
scene.screenshot(name="schematic_3d", scale=2)
scene.close()

# ---------------------------------------------------------------------------- #
#                                    2D plot                                   #
# ---------------------------------------------------------------------------- #
# get slices coordinates
coords_dict = bgh.get_structures_slice_coords(
    regions + ["TH"], orientation=plane_norm, position=plane_position,
)

f, ax = plt.subplots(figsize=(16, 10))
ax.axis("equal")
ax.axis("off")
ax.invert_yaxis()

# load image and show in the right position
ax.imshow(
    plt.imread("schematic_3d.png"),
    extent=[-5000, 8000, 5000, -2000],
    zorder=-10,
)

# plot 2D coordinates of thalamus subregions
for struct_name, contours in coords_dict.items():
    if struct_name == "root":
        continue
    elif struct_name == "TH":
        alpha, color, zorder = 1, grey, -2
        label = False
    elif "LG" in struct_name:
        alpha, color, zorder = 1, red_dark, 3
        label = True
    else:
        alpha, color, zorder = 1, grey_light, 2
        label = False

    for cont in contours:
        ax.fill(
            1.3 * cont[:, 0],
            1.3 * cont[:, 1],
            lw=1,
            fc=color,
            ec="k",
            zorder=zorder,
            alpha=alpha,
        )

        if label:
            # write outlined text to label each brain region
            txt = ax.text(
                1.3 * cont[:, 0].mean(),
                1.3 * cont[:, 1].mean(),
                struct_name,
                ha="center",
                va="center",
                fontsize=12,
            )
            txt.set_path_effects(
                [path_effects.withStroke(linewidth=6, foreground="white",)]
            )


f.savefig("schematic_2d.png")
plt.show()

os.remove("schematic_2d.png")
os.remove("schematic_3d.png")
