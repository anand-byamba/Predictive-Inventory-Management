import os
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert.preprocessors.execute import CellExecutionError

def run_notebook(notebook_path):
    print(f"--> Executing {notebook_path}...")
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)

    ep = ExecutePreprocessor(timeout=600, kernel_name='predictive_inventory_env')

    try:
        ep.preprocess(nb, {'metadata': {'path': os.path.dirname(notebook_path)}})
    except CellExecutionError as e:
        print(f"Error executing the notebook {notebook_path}.")
        print(e)
        raise

    # Save the executed notebook (optional, good for debugging)
    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print(f"--> Done: {notebook_path}")

def main():
    notebooks_dir = 'notebooks'
    notebooks = [
        '01_Data_Engineering.ipynb',
        '02_ABC_Analysis.ipynb',
        '03_Forecasting.ipynb',
        '04_Inventory_Optimization.ipynb',
        '05_Executive_Report.ipynb'
    ]

    print("=== Starting Inventory Management Pipeline ===")
    
    # Create results directory if it doesn't exist
    os.makedirs('results/figures', exist_ok=True)

    for nb_name in notebooks:
        nb_path = os.path.join(notebooks_dir, nb_name)
        if os.path.exists(nb_path):
            run_notebook(nb_path)
            
        else:
            print(f"Error: Notebook {nb_path} not found.")
            return

    print("=== Pipeline Completed Successfully ===")

if __name__ == "__main__":
    main()
