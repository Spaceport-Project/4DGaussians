ModelHiddenParams = dict(
    kplanes_config = {
     'grid_dimensions': 2,
     'input_coordinate_dim': 4,
     'output_coordinate_dim': 16,
     'resolution': [64, 64, 64, 150]
    },
    multires = [1,2,4,8],
    defor_depth = 2,
    net_width = 512,
    plane_tv_weight = 0.0002,
    time_smoothness_weight = 0.001,
    l1_time_planes =  0.0001,
    no_do=False,
    no_dshs=False,
    no_ds=False,
    empty_voxel=False,
    render_process=False,
    static_mlp=False,
)

OptimizationParams = dict(
    # optimized params
    # coarse_iterations = 4000,
    # iterations = 40_000,
    # densify_until_iter = 2700,
    # densify_from_iter = 1700,
    # net_width = 512,
    loss="l1",
    dataloader=True,
    opacity_reset_interval = 3000,
    densify_until_iter = 15_000, # default deger
    densify_from_iter = 500, # default deger
    iterations = 30_000,
    coarse_iterations = 7000,
    batch_size=1,
    deformation_lr_init = 0.00016,
    opacity_lr = 0.05, # default 0.05
    opacity_threshold_coarse = 0.005,
    opacity_threshold_fine_init = 0.005,
    opacity_threshold_fine_after = 0.005,
    # pruning_interval = 2000,
    # lambda_lpips=0.5,
    # lambda_dssim=0.5,
)