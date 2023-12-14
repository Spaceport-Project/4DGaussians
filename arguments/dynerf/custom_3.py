ModelHiddenParams = dict(
    render_process=False,
    kplanes_config = {
     'grid_dimensions': 2,
     'input_coordinate_dim': 4,
     'output_coordinate_dim': 16,
     'resolution': [64, 64, 64, 150]
    },
    multires = [1,2,4,8],
    defor_depth = 2,
    net_width = 256,
    plane_tv_weight = 0.0002,
    time_smoothness_weight = 0.001,
    l1_time_planes =  0.001,
    timebase_pe = 5,
    scale_rotation_pe = 2,
    timenet_width = 128,
    timenet_output = 64,

)
OptimizationParams = dict(
    batch_size = 2,
    dataloader=True,
    iterations = 60_000,
    coarse_iterations = 7000,
    densify_until_iter = 15_000,
    opacity_reset_interval = 20000,

    opacity_threshold_coarse = 0.005,
    opacity_threshold_fine_init = 0.005,
    opacity_threshold_fine_after = 0.005,
    # pruning_interval = 2000
)