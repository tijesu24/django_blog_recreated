
import Plugin from '@ckeditor/ckeditor5-core/src/plugin';
import ButtonView from '@ckeditor/ckeditor5-ui/src/button/buttonview';
import imageIcon from '@ckeditor/ckeditor5-core/theme/icons/image.svg';

export default class DjangoFilerImagePlugin extends Plugin {
    init() {
        const editor = this.editor;

        editor.ui.componentFactory.add('djangoFilerImage', locale => {
            const button = new ButtonView(locale);

            button.set({
                label: 'Insert image from Django Filer',
                icon: imageIcon,
                tooltip: true
            });

            button.on('execute', () => {
                // Open a dialog to browse django-filer images
                this.openImageBrowser();
            });

            return button;
        });
    }

    openImageBrowser() {
        // Make an AJAX request to your Django view
        fetch('/admin/filer/folder/last/?_pick=file&_to_field=file_ptr')
            .then(response => response.json())
            .then(data => {
                // Display the images in a dialog
                // When an image is selected, insert it into the editor
                this.editor.model.change(writer => {
                    const imageElement = writer.createElement('image', {
                        src: selectedImageUrl
                    });
                    this.editor.model.insertContent(imageElement);
                });
            });
    }
}