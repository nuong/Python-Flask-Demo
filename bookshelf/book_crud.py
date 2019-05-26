from bookshelf import get_model, oauth2, storage
from flask import Blueprint, current_app, redirect, render_template, request, \
    session, url_for, flash


crud = Blueprint('crud', __name__)


def upload_image_file(file):
    """
    Upload the user-uploaded file to Google Cloud Storage and retrieve its
    publicly-accessible URL.
    """
    if not file:
        return None

    public_url = storage.upload_file(
        file.read(),
        file.filename,
        file.content_type
    )

    current_app.logger.info(
        "Uploaded file %s as %s.", file.filename, public_url)

    return public_url


def get_types_selection(book):
    types = get_model().list_types()
    types_of_books = []
    if 'types' in book:
        types_of_books = book['types']
    type_ids = [b_type['id'] for b_type in types]
    for book_type in types_of_books:
        if book_type in type_ids:
            type_index = type_ids.index(book_type)
            types[type_index]['selected'] = True
    return types


@crud.route("/")
def list():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    books, next_page_token = get_model().list(cursor=token)

    return render_template(
        "list.html",
        books=books,
        next_page_token=next_page_token)


# [START list_mine]
@crud.route("/mine")
@oauth2.required
def list_mine():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    books, next_page_token = get_model().list_by_user(
        user_id=session['profile']['email'],
        cursor=token)

    return render_template(
        "my-books.html",
        books=books,
        next_page_token=next_page_token)
# [END list_mine]


@crud.route('/<id>')
def view(id):
    book = get_model().read(id)
    return render_template("view.html", book=book)


# [START add]
@crud.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
            types = get_model().list_types()
            return render_template("form.html", action="Add", book={}, types=types)

        data = request.form.to_dict()
        types = request.form.getlist('types')
        data['types'] = types or []

        # If an image was uploaded, update the data to point to the new image.
        image_url = upload_image_file(request.files.get('image'))

        if image_url:
            data['imageUrl'] = image_url

        current_app.logger.info(data['types'])
        # If the user is logged in, associate their profile with the new book.
        if 'profile' in session:
            data['createdBy'] = session['profile']['name']
            data['createdById'] = session['profile']['email']

        book = get_model().create(data)

        return redirect(url_for('.view', id=book['id']))
    else:
        types = get_model().list_types()
        return render_template("form.html", action="Add", book={}, types=types)
# [END add]


@crud.route('/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    book = get_model().read(id)
    if book:
        current_user_id = session['profile']['email']
        book_created_id = book.get('createdById')
        if current_user_id and current_user_id == book_created_id:
            if request.method == 'POST':
                title = request.form['title']
                error = None

                if not title:
                    error = 'Title is required.'

                if error is not None:
                    flash(error)
                    types = get_types_selection(book)
                    return render_template("form.html", action="Edit", book=book, types=types)

                types = request.form.getlist('types')
                data = request.form.to_dict(flat=True)
                data['types'] = types or []

                image_url = upload_image_file(request.files.get('image'))

                if image_url:
                    data['imageUrl'] = image_url

                book = get_model().update(data, id)

                return redirect(url_for('.view', id=book['id']))
            else:
                types = get_types_selection(book)
                return render_template("form.html", action="Edit", book=book, types=types)
        else:
            return redirect('/403')
    else:
        return redirect('/404')


@crud.route('/<id>/delete')
def delete(id):
    get_model().delete(id)
    return redirect(url_for('.list'))


