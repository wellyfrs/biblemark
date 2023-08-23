/**
 * Matches [Bootstrap contextual classes](https://getbootstrap.com/docs/5.2/components/alerts)
 */
const NotificationContext = {
    PRIMARY: 'primary',
    SECONDARY: 'secondary',
    SUCCESS: 'success',
    DANGER: 'danger',
    WARNING: 'warning',
    INFO: 'info',
    LIGHT: 'light',
    DARK: 'dark',
}

const NOTIFICATION_CONTEXT_CLASS_PREFIX = 'text-bg-';

/**
 * Displays notifications.
 */
export default class NotifierView {
    constructor() {
        this.toastContainer = document.getElementById('toast-container');
        this.toastTemplate = document.getElementById('toast-template');
    }

    /**
     * Displays error toast.
     * @param {string} message
     * @param {string} [title=Error]
     */
    notifyError = (message, title = "Error") => {
        this._notify(message, title, NotificationContext.DANGER);
    }

    /**
     * Displays notification toast.
     * @param {string} message
     * @param {string} [title=Error]
     * @param {NotificationContext} [context=NotificationContext.INFO]
     * @private
     */
    _notify = (message, title = 'Info', context = NotificationContext.INFO) => {
        const toastElement = this.toastTemplate.content.cloneNode(true).querySelector('.toast');
        toastElement.classList.add(`${NOTIFICATION_CONTEXT_CLASS_PREFIX}${context}`);
        toastElement.querySelector('.toast-title').innerText = title;
        toastElement.querySelector('.toast-body').innerText = message;

        this.toastContainer.appendChild(toastElement);

        const toast = new bootstrap.Toast(toastElement);
        toast.show();
    }
}