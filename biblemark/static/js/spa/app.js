import Model from "./model/model.js";
import View from "./view/view.js";
import Client from "./client.js";
import NavView from "./view/navView.js";
import Controller from "./controller/controller.js";
import ControlView from "./view/controlView.js";
import BibleView from "./view/bibleView.js";
import NotifierView from "./view/notifierView.js";

const MAX_COLORS = 5;
const COLOR_CODE_FORMAT = /^#[0-9a-f]{6}$/i;

class App {

    /**
     * @typedef Config
     * @type {object}
     * @property {string} baseUrl
     * @property {Location} defaultLocation
     * @property [ColorDefinition] colors
     */

    /**
     * @typedef Location
     * @type {object}
     * @property {string} versionId
     * @property {string} bookId
     * @property {string} chapterId
     */

    /**
     * @typedef ColorDefinition
     * @type {object}
     * @property {string} code
     * @property {string} name
     */

    /**
     * @param {Config} config
     */
    constructor(config = {}) {
        const defaultConfig = {
            baseUrl: 'http://localhost',
            defaultLocation: {
                versionId: 'KJV',
                bookId: 'JHN',
                chapterId: '1'
            },
            colors: [
                { code: '#ffff00', name: 'Yellow' },
                { code: '#90ee90', name: 'Green' },
                { code: '#ffb6c1', name: 'Pink' },
                { code: '#add8e6', name: 'Blue' },
                { code: '#f08080', name: 'Red' },
            ],
        };

        this.config = {...defaultConfig, ...config}
        this._validateConfig();

        this.model = new Model();
        this.view = new View(new NavView(), new BibleView(), new ControlView(this.config.colors), new NotifierView());
        this.client = new Client(this.config.baseUrl);
        this.controller = new Controller(this.model, this.view, this.client);

        const { versionId, bookId, chapterId } = this._getLocation();
        this.controller.init(versionId, bookId, chapterId);
    }

    _validateConfig() {
        const { baseUrl, defaultLocation, colors } = this.config;

        if (typeof baseUrl !== 'string' || baseUrl === '') {
            throw new Error('Invalid base URL');
        }

        const isValidLocation = location => {
            const { versionId, bookId, chapterId } = location;
            return [versionId, bookId, chapterId].every(item => item && typeof item === 'string');
        }

        if (!defaultLocation || !isValidLocation(defaultLocation)) {
            throw new Error('Invalid default location');
        }

        const isValidColor = color => {
            const { code, name } = color;
            return (code && COLOR_CODE_FORMAT.test(code) && typeof name === 'string' && name !== '');
        }

        if (!Array.isArray(colors) || colors.length === 0 || colors.length > MAX_COLORS || !colors.every(isValidColor)) {
            throw new Error('Invalid colors');
        }
    }

    _getLocation = () => {
        const [, versionIdParam, bookIdParam, chapterIdParam] = window.location.pathname.split('/');

        const versionId = versionIdParam || this.config.defaultLocation.versionId;
        const bookId = bookIdParam || this.config.defaultLocation.bookId;
        const chapterId = chapterIdParam || this.config.defaultLocation.chapterId;

        return { versionId, bookId, chapterId }
    }
}

new App({
    baseUrl: "http://127.0.0.1:5000"
});
