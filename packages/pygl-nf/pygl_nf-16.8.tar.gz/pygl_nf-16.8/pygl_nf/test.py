import GL

win = GL.Display_init(flags='NONE')


m = GL.Sub_events_.Mouse_init()

while win.CLOSE():
    win.UPDATE().SETBGCOLOR() ; win.UPDATE_SCREEN()
    if m.GET_PRESS_ON_PYGL_WINDOW():win.SET_NONE()
    elif m.GET_PRESS_ON_PYGL_WINDOW('r'):win.SET_RESIZE()

    win.GL.Rect('blue',[200,150],[185,100],0,'s','D')