from src.virtual_assistant.assistant import VirtualAssistant


def main():
    assistant = VirtualAssistant(audio_on=True, open_webpages=True)
    assistant.greet()
    assistant.print_commands()
    assistant.activate()


if __name__ == "__main__":
    main()
