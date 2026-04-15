from app_design import AppDesign
from app_logic import AppLogic

def main():
    app_logic = AppLogic()
    app_design = AppDesign(app_logic)
    app_design.run()

if __name__ == "__main__":
    main()