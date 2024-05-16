def mongo_conector(setup_state):
    global mongo_db
    mongo_db = setup_state.app.config['mongo']