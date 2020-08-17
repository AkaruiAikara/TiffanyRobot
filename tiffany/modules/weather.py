import pyowm
from telegram.ext import run_async

from tiffany import dispatcher, API_WEATHER, BAN_STICKER
from tiffany.modules.disable import DisableAbleCommandHandler


@run_async
def weather(bot, update, args):
    if len(args) == 0: 
        update.effective_message.reply_text(
            "Write a location to check the weather.")
        return

    location = " ".join(args)
    if location.lower() == bot.first_name.lower():
        update.effective_message.reply_text(
            "I will keep an eye on both happy and sad times!")
        bot.send_sticker(update.effective_chat.id, BAN_STICKER)
        return

    try:
        owm = pyowm.OWM(API_WEATHER)
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(location)
        wtr = observation.weather
        thetemp = wtr.temperature(unit='fahrenheit').get('temp')
        if thetemp is None:
            thetemp = "Unknown"

        # Weather symbols
        status = ""
        status_now = wtr.weather_code
        if status_now < 232:  # Rain storm
            status += "⛈️ "
        elif status_now < 321:  # Drizzle
            status += "🌧️ "
        elif status_now < 504:  # Light rain
            status += "🌦️ "
        elif status_now < 531:  # Cloudy rain
            status += "⛈️ "
        elif status_now < 622:  # Snow
            status += "🌨️ "
        elif status_now < 781:  # Atmosphere
            status += "🌪️ "
        elif status_now < 800:  # Bright
            status += "🌤️ "
        elif status_now < 801:  # A little cloudy
            status += "⛅️ "
        elif status_now < 804:  # Cloudy
            status += "☁️ "
        status += wtr.detailed_status

        update.message.reply_text(
            "Today in {} is being {}, around {}°F.\n".format(
                location, status, thetemp))

    except pyowm.exceptions.api_response_error:
        update.effective_message.reply_text("Sorry, location not found.")


__help__ = """
 - /weather <city>: get weather info in a particular place
"""

__mod_name__ = "Weather"

WEATHER_HANDLER = DisableAbleCommandHandler("weather", weather, pass_args=True)

dispatcher.add_handler(WEATHER_HANDLER)
