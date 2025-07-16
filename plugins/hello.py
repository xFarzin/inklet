def register(app):
    #app.__init__()
    app.addCommand("Say Hello", lambda: print("👋 Plugin says hello!"))
