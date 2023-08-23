/**
 * View for the user controls for highlights and notes.
 */
export default class ControlView {

    constructor(colorDefinitions) {
        this.colorDefinitions = colorDefinitions;

        this.container = document.getElementById('marking-control');

        this.highligthControls = document.getElementById('highlight-control');
        this.highlightBtnTpl = document.getElementById('tpl-btn-highlight');

        this.noteModalContainer = document.getElementById('note-modal');
        this.noteModal = new bootstrap.Modal(this.noteModalContainer);
        this.noteTextarea = document.getElementById('note-textarea');
        this.noteBtn = document.getElementById('btn-note');

        this.noteModalContainer.addEventListener('shown.bs.modal', event => {
            this._onNoteModalOpen(event);
        });
    }

    close() {
        this.container.classList.add('d-none');
        this.noteModal.hide();
    }

    /**
     * @param {[string]} selectedHighlightedVerseColors
     */
    render(selectedHighlightedVerseColors) {
        this.container.classList.remove('d-none');
        this.noteTextarea.value = '';
        this.highligthControls.innerHTML = '';

        this.colorDefinitions.forEach(colorDefinition => {
            const btn = this.highlightBtnTpl.content.cloneNode(true).querySelector('button');
            btn.dataset.colorName = colorDefinition.name;
            btn.dataset.colorCode = colorDefinition.code;
            btn.style.backgroundColor = colorDefinition.code;

            if (selectedHighlightedVerseColors.includes(colorDefinition.code)) {
                btn.classList.add('remove');
                btn.querySelector('.color-name').innerText = `Remove ${colorDefinition.name.toLowerCase()}`;
            } else {
                btn.querySelector('.color-name').innerText = colorDefinition.name;
            }

            btn.addEventListener('click', event => {
                this.highligthHandler(event.target.dataset.colorCode);
            });

            this.highligthControls.appendChild(btn);
        });
    }

    /**
     * @param {highlightActionHandlerCallback} handler
     */
    bindHighlightAction = handler => this.highligthHandler = handler;

    /**
     * @param {addNoteHandlerCallback} handler
     */
    bindAddNoteAction = handler =>
        this.noteBtn.addEventListener('click', event => handler(this.noteTextarea.value));

    /**
     * Autofocus textarea after opening the note addition modal.
     * @param {Event} event
     * @private
     */
    _onNoteModalOpen = event => {
        this.noteTextarea.focus();
    }
}