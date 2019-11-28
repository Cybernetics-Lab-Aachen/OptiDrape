params = {
    'model': {
        'fixed_x': 1400,
        'fixed_y': 1400,
        'n_hidden_1': 1024,
        'n_hidden_2': 256,
        'l1_filters': 8,
        'l2_filters': 8,
        'l3_filters': 8,
        'l1_kernel': [2, 2],
        'l2_kernel': [2, 2],
        'l3_kernel': [2, 2],
        'l1_dropout': 0.7,
        'l2_dropout': 0.7,
        'l3_dropout': 0.7,
        'l4_dropout': 0.5,
        'l4_units': 512,
        'l5_units': 256,
        'batch_size': 128,
        'epochs':  1000,
        'learning_rate': 0.001,
        'save_file': 'PyramideModel',
        'input_dir': '/home/matthias/Workspace/optidrapefix/res/Pyramide/geometry',
    },
    'data': {
        'geometry_dir': '/home/matthias/Workspace/optidrapefix/res/Pyramide/geometry',
        'label_dir': '/home/matthias/Workspace/optidrapefix/res/Pyramide/label',
        'threshold': 1.0,
        'weight_max_angle': 0.4,
        'scale': 1.0,
    }
}