from utils.driver_manager import get_driver


def before_scenario(context, scenario):
    print("Before Scenario")
    context.driver = get_driver()


def after_scenario(context, scenario):
    print("After Scenario")
    context.driver.quit()


def after_step(context, step):
    print("After Step")
