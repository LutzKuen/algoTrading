from observer import controller
cont = controller.controller('/home/ubuntu/settings_triangle.conf',None)
cont.data2sheet(newEstim = True, write_predict = False, write_raw = False)
