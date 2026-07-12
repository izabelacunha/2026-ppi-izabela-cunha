from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('fornecedor', __name__)


@bp.route('/')
def index():
    db = get_db()
    fornecedores = db.execute(
        '''
        SELECT f.id, nome, telefone, servico, created, author_id, username
        FROM fornecedor f
        JOIN user u ON f.author_id = u.id
        ORDER BY created DESC
        '''
    ).fetchall()

    return render_template('fornecedor/index.html', fornecedores=fornecedores)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        servico = request.form['servico']

        error = None

        if not nome:
            error = 'O nome é obrigatório.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                '''
                INSERT INTO fornecedor
                (nome, telefone, servico, author_id)
                VALUES (?, ?, ?, ?)
                ''',
                (nome, telefone, servico, g.user['id'])
            )
            db.commit()

            return redirect(url_for('fornecedor.index'))

    return render_template('fornecedor/create.html')


def get_fornecedor(id, check_author=True):
    fornecedor = get_db().execute(
        '''
        SELECT f.id, nome, telefone, servico,
               created, author_id, username
        FROM fornecedor f
        JOIN user u ON f.author_id = u.id
        WHERE f.id = ?
        ''',
        (id,)
    ).fetchone()

    if fornecedor is None:
        abort(404, "Fornecedor não encontrado.")

    if check_author and fornecedor['author_id'] != g.user['id']:
        abort(403)

    return fornecedor


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    fornecedor = get_fornecedor(id)

    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        servico = request.form['servico']

        error = None

        if not nome:
            error = 'O nome é obrigatório.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                '''
                UPDATE fornecedor
                SET nome = ?,
                    telefone = ?,
                    servico = ?
                WHERE id = ?
                ''',
                (nome, telefone, servico, id)
            )
            db.commit()

            return redirect(url_for('fornecedor.index'))

    return render_template(
        'fornecedor/update.html',
        fornecedor=fornecedor
    )


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_fornecedor(id)

    db = get_db()
    db.execute(
        'DELETE FROM fornecedor WHERE id = ?',
        (id,)
    )
    db.commit()

    return redirect(url_for('fornecedor.index'))