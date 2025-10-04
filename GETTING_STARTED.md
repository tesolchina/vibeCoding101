# Getting Started with Vibe Coding 101 🚀

This guide will help you set up your environment and get started with the workshop.

## Step 1: Install Python

### Windows
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **Important**: Check "Add Python to PATH" during installation
4. Verify installation: Open Command Prompt and type `python --version`

### Mac
1. Python 3 is often pre-installed. Check by typing `python3 --version` in Terminal
2. If not installed, download from [python.org](https://www.python.org/downloads/)
3. Or install via Homebrew: `brew install python3`

### Linux
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
```

## Step 2: Clone the Repository

```bash
git clone https://github.com/tesolchina/vibeCoding101.git
cd vibeCoding101
```

Or download as ZIP from GitHub and extract it.

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

If you have both Python 2 and 3 installed, use:
```bash
pip3 install -r requirements.txt
```

## Step 4: Launch Jupyter Notebook

```bash
jupyter notebook
```

This will open your web browser with the Jupyter interface.

## Step 5: Open the Notebook

1. In the Jupyter interface, click on `vibeCoding101.ipynb`
2. The notebook will open in a new tab
3. Follow along with the instructions in the notebook

## Using the Notebook

### Running Code Cells
- Click on a cell to select it
- Press `Shift + Enter` to run the cell
- Or click the "Run" button in the toolbar

### Editing Code Cells
- Click on a code cell to edit it
- Modify the code as you like
- Run it to see your changes

### Adding New Cells
- Click the `+` button in the toolbar
- Or use keyboard shortcuts:
  - `A` - insert cell above
  - `B` - insert cell below

## Getting GitHub Copilot (Optional but Recommended)

GitHub Copilot is an AI assistant that helps you write code. It's free for students!

### For Students
1. Get the [GitHub Student Developer Pack](https://education.github.com/pack)
2. This includes free GitHub Copilot
3. Install the [GitHub Copilot extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) for VS Code or your IDE

### Using Copilot in Jupyter
While Copilot works best in IDEs like VS Code, you can still use the vibe coding approach:
1. Think about what you want to do
2. Describe it in plain English as a comment
3. Try to write the code based on what you've learned
4. Test and refine

## Troubleshooting

### "jupyter: command not found"
Make sure you've installed the requirements:
```bash
pip install jupyter notebook
```

### Import Errors
If you get import errors, reinstall the requirements:
```bash
pip install -r requirements.txt --upgrade
```

### Port Already in Use
If port 8888 is already in use:
```bash
jupyter notebook --port 8889
```

### Python Version Issues
Make sure you're using Python 3.8 or higher:
```bash
python3 --version
```

## Tips for Success

### Start Simple
Don't try to understand everything at once. Focus on one concept at a time.

### Experiment
Change values, try different inputs, and see what happens. You can't break anything!

### Take Notes
Use markdown cells to add your own notes and observations.

### Ask Questions
If using Copilot or another AI assistant, don't hesitate to ask questions like:
- "How does this code work?"
- "What does this function do?"
- "Can you explain this concept?"

### Practice Regularly
Coding is a skill. Practice a little bit every day for best results.

## Need Help?

- Check the notebook itself - it has lots of explanations
- Search for error messages online
- Ask in the GitHub Issues section
- Talk to your workshop instructor

## Ready to Start?

Open `vibeCoding101.ipynb` and begin your coding journey! 🎉

Remember: **Everyone starts as a beginner. The only way to learn is to start!**
