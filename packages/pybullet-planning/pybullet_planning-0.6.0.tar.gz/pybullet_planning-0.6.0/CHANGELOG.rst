
Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

Unreleased
----------

**Added**

**Changed**

**Fixed**

**Deprecated**

**Removed**

Known Unresolved Issues
-----------------------

- `get_body_collision_vertices` does not support cloned body now. We don't have a good way to do catch-throw for this now.
- Cloning body from an already cloned body introduces unexpected result (visual or collision data erased etc).

0.6.0
----------

**Added**
- Added `distance_threshold` to `pairwise_link_collision_info` and `pairwise_link_collision` to allow collision checking given a penetration threshold
- Added `sweep_collision_fn` to `birrt` to allow sweep collision check in edge expansion
- Added `coarse_waypoints` to the `smooth_path` function to give options for use refined shortcut to ensure collision-free results.
- `LOGGER` introduced to replace `print`
- Added `get_data_filename_and_height` to include cached mesh filename and scale from `get_model_info`
- Added `CreateVisualArray` and `CreateCollisionArray` for `visual_shape_from_data` and `visual_shape_from_data`. We use the new `get_data_filename_and_height` when file_name is `UNKNOWN_FILE`.
- Added `load_pybullet` support for `stl` files by `create_obj`.
- Added `get_body_collision_vertices` for getting body collision vertices in its current configuration.

**Changed**
- Apply `HideOutput` to pybullet IK error printouts in `inverse_kinematics_helper`
- ``motion_planners`` module up-to-date with commit `e6f23053e <https://github.com/caelan/motion-planners/commit/e6f23053e441af091b898b7f56c6fee48223be48>`_.
- Changed the mesh reading procedure in `vertices_from_data` from `pp.read_obj` to `meshio.read`. This fixes #9.
- `smooth_path`'s `max_iterations` argument changed to `max_smooth_iterations`
- 'set_color' defaulted to set the color of all the links of body.
- `vertices_from_data` get filename and **scale** from cached `INFO_FROM_BODY` (through `get_data_filename_and_height`) if the data's filename does not end with `.urdf`

**Fixed**
- Fixed `read_obj` returns empty dict if obj file does not start with objects (``o object_name``)
- Fixed `get_extend_fn(q1,q2)` to include `q1` in its output path. This bug was causing incorrect planning result in birrt, because the two trees will have a gap in the middle that is unchecked.
- Fixed a minor mesh vertex scaling bug in `vertices_from_data`
- catch `get_num_joints(body) == 0` when a rigid body without joint and link are passed to `clone_body`
- clear `INFO_FROM_DATA` when `disconnect` or `reset_simulation`

0.5.1
----------

**Added**
- Added `current_conf` to as the single-node ladder in the ladder graph Cartesian planning `plan_cartesian_motion_lg`

**Changed**
- Changed `Attachment.from_data` to construct parent and child bodies from body name data
- Changed `EdgeBuilder` from using `upper_tm` and `joint_vel_limits` to directly using `jump_threshold`

0.5.0
----------

**Changed**

* Changed doc theme to sphinx-rtd-theme, doc hosted on readthedocs
* Changed `motion_planners` to keep updated with https://github.com/caelan/motion-planners

**Added**

* Added `SE3` floating body motion planning
* Added ladder graph cartesian planner

**Removed**

* Removed `requirments.txt`, moved dependencies into `setup.py`

0.1.1
----------

**Fixed**

* Fixed Windows OS "Display not in os.environ" issue in `connect`


0.1.0
----------

**Added**

* diagnosis collision checking function to help visualizing the collision bodies' information
* add `workspace_bodies` to the `get_collision_fn` to check collisions with the obstacles specified in a URDF file.
* move `ik_interface` module from application side to this repo, since it's "universal" for fixed-end robot. Might need to add a separete one for robots with moving base later.
* enable travis ci unit test, collision_fn well tested
* `get_floating_body_collision_fn` to check a body without joints's collision. Associated test added.
* Added `snap_sols` to `kinematics.ik_utils`

**Changed**

* add `extra_disabled_collisions` parameter to `get_collision_fn`, `plan_joint_motion`
* Changed `get_name` to return name without index if name is not `''`

**Removed**

* `get_collision_diagnosis_fn` removed, integrated into the `get_collision_fn`

**Fixed**

* `utils.numeric_sample.randomize`: `random.shuffle` cannot operate on a `range` in py 3.x. Enforced conversion to `list` to fix it.
* Fixed `get_collision_fn` to ignore checking between bodies both specified in attachment and obstacles (prioritize its role as attachment)

**Deprecated**

**TODO**

* add body name for bodies from `create_obj`

**Requested features**

* `clone_body` work for bodies from `create_obj`


0.0.1
-------

**Added**

* Initial version
* Divide the original `utils.py` file into separate modules
* Modules cycle dependency resolved.

