from utils.driver_manager import get_driver


def before_scenario(context, scenario):
    print(f"Before Scenario {scenario}")
    context.driver = get_driver()


def after_scenario(context, scenario):
    print(f"After Scenario {scenario}")
    context.driver.quit()


def before_step(context, step):
    print(f"Before Step {step}")
    context.step_name = step.name


def after_step(context, step):
    print(f"After Step {step}")
