<h2 align="center">The Animal API</h2>

<p align="center">
    <img src="static/favicon_256x.ico" alt="favicon" width="64" height="64">
</p>

<br>

<p align="center">
    <img src="https://img.shields.io/github/created-at/henrique-coder/theanimalapi?style=for-the-badge&logoColor=white&labelColor=gray&color=white" alt="GitHub Created At">
    <img src="https://img.shields.io/github/commit-activity/m/henrique-coder/theanimalapi?style=for-the-badge&logoColor=white&labelColor=gray&color=white" alt="GitHub commit activity">
    <img src="https://img.shields.io/github/last-commit/henrique-coder/theanimalapi?style=for-the-badge&logoColor=white&labelColor=gray&color=white" alt="GitHub last commit">
</p>

<p align="center">
    An API that returns random photos of more than 50 different types of animals, in a total of more than 50,000 selected photos.
</p>

<br>

#### Features
- Has a Discord bot that can be added to any server. You can invite it [here](https://discord.com/api/oauth2/authorize?client_id=1109094043423608853&permissions=2048&scope=bot%20applications.commands) (temporarily offline).
- Has interactive documentation.
- Return random photos of a variety of animals.
- Return photos of a specific animal.

#### How to use

Basically, you can access the API through the base API URL and add the parameters you want to use.

- Interactive documentation: https://theanimalapi.onrender.com/docs
- Base API URL: https://theanimalapi.onrender.com/api/v1/search/animal

Parameters:

- **`name`** (optional): the name of the animal you want to search for.

#### How was it done?

- Built with [Python 3.13.2](https://www.python.org/downloads/release/python-3132)
- Uses [FastAPI](https://fastapi.tiangolo.com) as the web framework.

### Installation from source code

```bash
# 1. Clone the repository
git clone https://github.com/henrique-coder/theanimalapi.git

# 2. Change the directory
cd theanimalapi

# 3. Install the requirements
pip install --upgrade -r requirements.txt

# 4. Run the web server
uvicorn theanimalapi:app --reload  # Development
uvicorn theanimalapi:app  # Production
```

### Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have any suggestions that could improve this project, please [fork](https://github.com/henrique-coder/theanimalapi/fork) the repository and open a pull request. Or simply open an [issue](https://github.com/henrique-coder/theanimalapi/issues/new) and describe your ideas or let us know what bugs you've found. Don't forget to give the project a star. Thanks again!

1. Fork the project at https://github.com/henrique-coder/theanimalapi/fork
2. Create your feature branch ・ `git checkout -b feature/{feature_name}`
3. Commit your changes ・ `git commit -m "{commit_message}"`
4. Push to the branch ・ `git push origin feature/{feature_name}`
5. Open a pull request describing the changes made and detailing the new feature. Then wait for an administrator to review it and you're done!

### License

Distributed under the **MIT License**. See [LICENSE](https://github.com/henrique-coder/theanimalapi/blob/main/LICENSE) for more information.

### Disclaimer

Please note that this project is still under development and may contain errors or incomplete functionality. If you encounter any problems, feel free to open an [issue](https://github.com/henrique-coder/theanimalapi/issues/new) and describe the problem you are facing. Your feedback is very important to us.
