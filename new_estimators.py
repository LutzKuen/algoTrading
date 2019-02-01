try:
    from observer import controller_cython as controller
    # from observer import controller as controller
except ImportError:
    print('WARNING: Cython module not found, falling back to native python')
    from observer import controller as controller
cont = controller.Controller('../settings_dev.conf', 'demo', verbose=1)
cont.data2sheet(write_predict=False, read_raw=True, write_raw=False, improve_model=True)
