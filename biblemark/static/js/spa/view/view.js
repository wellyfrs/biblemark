/**
 * Wrapper for view classes.
 */
export default class View {

    /**
     * @param {NavView} nav - Component for Bible navigation.
     * @param {BibleView} bible - Component for rendering Bible content and marks.
     * @param {ControlView} control - Component for creating, editing, and updating marks.
     * @param {NotifierView} notifier - Component for displaying notifications.
     */
    constructor(nav, bible, control, notifier) {
        this.nav = nav;
        this.bible = bible;
        this.control = control;
        this.notifier = notifier;
    }
}