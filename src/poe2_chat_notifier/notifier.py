import platform

if platform.system() == 'Windows':
    import winsound
    from win32gui import GetForegroundWindow, GetWindowText
    import windows_toasts


MESSAGES_TO_KEEP_ = 3


class Notifier:
    '''Game-aware notifier.'''
    def __init__(self):
        pass

    def notify(self, message: str, always_play_sound: bool):
        '''Sends a notification showing recent messages.'''
        pass


class NotifierWindows(Notifier):
    def __init__(self):
        self.toaster_ = windows_toasts.WindowsToaster('PoE2 Chat')
        self.toast_ = windows_toasts.Toast()
        self.toast_.duration = windows_toasts.ToastDuration.Short
        self.messages_ = []

    def notify(self, message: str, always_play_sound: bool):
        if len(self.messages_) >= MESSAGES_TO_KEEP_:
            self.messages_.pop(0)
        self.messages_.append(message)
        toast_text = ''
        for message in self.messages_:
            toast_text += f'{message}\n'
        self.toast_.text_fields = [toast_text]

        # FIXME: This focus check isn't guaranteed to work since another
        # program could use the same text.
        if 'Path of Exile 2' == GetWindowText(GetForegroundWindow()):
            # Don't want to put a notification box over the game.
            self.toaster_.update_toast(self.toast_)
            if always_play_sound:
                self.sound_notification()
        else:
            self.toaster_.show_toast(self.toast_)

    def sound_notification(self):
        winsound.PlaySound('Notification',
                           winsound.SND_ALIAS | winsound.SND_ASYNC)


def create_notifier() -> Notifier:
    '''Create a Notifer for the current OS.'''
    if platform.system() == 'Windows':
        return NotifierWindows()
    else:
        return Notifier()
