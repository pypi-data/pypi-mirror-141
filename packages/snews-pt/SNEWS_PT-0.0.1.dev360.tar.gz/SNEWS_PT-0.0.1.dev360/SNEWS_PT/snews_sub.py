
import os, json, click
from hop import Stream
from . import snews_pt_utils

def make_file(outputfolder):
    """ Get a proper json file name at a given folder
    """
    os.makedirs(outputfolder, exist_ok=True)
    S = Subscriber()
    file = os.path.join(outputfolder, f"0_{S.times.get_date()}_ALERTS.json")
    # if file exists make a new
    # TODO: do it properly
    if os.path.isfile(file):
        # i = file.split('/')[-1][0]
        file = os.path.join(outputfolder, f"1_{S.times.get_date()}_ALERTS.json")
    return file

def save_message(message, outputfolder):
    """ Save messages to a json file.

    """
    file = make_file(outputfolder)
    with open(file, 'w') as outfile:
        json.dump(message, outfile, indent=4, sort_keys=True)


def display(message):
    """ Function to format output messages
    """
    click.echo(click.style('ALERT MESSAGE'.center(65, '_'), bg='red', bold=True))
    for k, v in message.items():
        if type(v) == type(None): v = 'None'
        if type(v) == int:
            click.echo(f'{k:<20s}:{v:<45}')
        if type(v) == str:
            click.echo(f'{k:<20s}:{v:<45}')
        elif type(v) == list:
            v = [str(item) for item in v]
            items = '\t'.join(v)
            if k == 'detector_names':
                click.echo(f'{k:<20s}' + click.style(f':{items:<45}', bg='blue'))
            else:
                click.echo(f'{k:<20s}:{items:<45}')
    click.secho('_'.center(65, '_'), bg='bright_red')

class Subscriber:
    """ Class to subscribe ALERT message stream

    Parameters
    ----------
    env_path : `str`
        path for the environment file.
        Use default settings if not given

    """
    def __init__(self, env_path=None):
        snews_pt_utils.set_env(env_path)
        self.obs_broker = os.getenv("OBSERVATION_TOPIC")
        self.alert_topic = os.getenv("ALERT_TOPIC")
        self.times = snews_pt_utils.TimeStuff()

        # time object/strings
        self.times = snews_pt_utils.TimeStuff(env_path)
        self.hr = self.times.get_hour()
        self.date = self.times.get_date()
        self.snews_time = lambda: self.times.get_snews_time()
        self.default_output = os.path.join(os.getcwd(), os.getenv("ALERT_OUTPUT"))


    def subscribe(self, outputfolder=None):
        """ Subscribe and listen to a given topic

        Parameters
        ----------
        outputfolder: `str`
            where to save the alert messages, if None
            creates a file based on env file

        """
        outputfolder = outputfolder or self.default_output
        # base = os.path.dirname(os.path.realpath(__file__))
        # outputfolder = os.path.join(base, outputfolder)
        click.echo('You are subscribing to ' +
                   click.style(f'ALERT', bg='red', bold=True) + '\nBroker:' +
                   click.style(f'{ self.alert_topic}', bg='green'))

        # Initiate hop_stream
        stream = Stream(until_eos=False)
        try:
            with stream.open(self.alert_topic, "r") as s:
                for message in s:
                    save_message(message, outputfolder)
                    snews_pt_utils.display_gif()
                    display(message)
        except KeyboardInterrupt:
            click.secho('Done', fg='green')


    def subscribe_and_redirect_alert(self, outputfolder=None):
        """ subscribe generator
        """
        outputfolder = outputfolder or self.default_output
        # base = os.path.dirname(os.path.realpath(__file__))
        # outputfolder = os.path.join(base, outputfolder)
        click.echo('You are subscribing to ' +
                   click.style(f'ALERT', bg='red', bold=True) + '\nBroker:' +
                   click.style(f'{ self.alert_topic}', bg='green'))

        # Initiate hop_stream
        stream = Stream(until_eos=False)
        try:
            with stream.open(self.alert_topic, "r") as s:
                for message in s:
                    save_message(message, outputfolder)
                    snews_pt_utils.display_gif()
                    display(message)
                    # jsonformat = json.dumps(message)
                    yield make_file(outputfolder)
        except KeyboardInterrupt:
            click.secho('Done', fg='green')
