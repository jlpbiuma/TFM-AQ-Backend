from api.create_app import MyApp

app = MyApp()  # Create an instance of MyApp

if __name__ == "__main__":
    # host the app on port 5000
    app.run(debug=True, port=5000, threaded=True, host='0.0.0.0')
