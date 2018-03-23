import pytest
from datetime import datetime
from uuid import uuid4

from catalog_persistence.databases import DocumentNotFound
from catalog_persistence.models import get_record, RecordType


def get_article_record(content={'Test': 'Test'}):
    document_id = uuid4().hex
    return get_record(document_id=document_id,
                      document_type=RecordType.ARTICLE,
                      content=content,
                      created_date=datetime.utcnow())


def test_register_document(setup, database_service):
    article_record = get_article_record()
    database_service.register(
        article_record['document_id'],
        article_record
    )

    check_list = database_service.find()
    assert isinstance(check_list[0], dict)
    article_check = check_list[0]
    assert article_check['document_id'] == article_record['document_id']
    assert article_check['document_type'] == article_record['document_type']
    assert article_check['content'] == article_record['content']
    assert article_check['created_date'] is not None


def test_read_document(setup, database_service):
    article_record = get_article_record({'Test': 'Test2'})
    database_service.register(
        article_record['document_id'],
        article_record
    )

    record_check = database_service.read(article_record['document_id'])
    assert record_check is not None
    assert record_check['document_id'] == article_record['document_id']
    assert record_check['document_type'] == article_record['document_type']
    assert record_check['content'] == article_record['content']
    assert record_check['created_date'] is not None


def test_read_document_not_found(setup, database_service):
    pytest.raises(
        DocumentNotFound,
        database_service.read,
        '336abebdd31894idnaoexistente'
    )


def test_update_document(setup, database_service):
    article_record = get_article_record({'Test': 'Test3'})
    database_service.register(
        article_record['document_id'],
        article_record
    )

    article_update = database_service.read(article_record['document_id'])
    article_update['content'] = {'Test': 'Test3-updated'}
    database_service.update(
        article_record['document_id'],
        article_update
    )

    record_check = database_service.read(article_record['document_id'])
    assert record_check is not None
    assert record_check['document_id'] == article_update['document_id']
    assert record_check['document_type'] == article_update['document_type']
    assert record_check['content'] == article_update['content']
    assert record_check['created_date'] is not None
    assert record_check['updated_date'] is not None


def test_update_document_not_found(setup, database_service):
    article_record = get_article_record({'Test': 'Test4'})
    pytest.raises(
        DocumentNotFound,
        database_service.delete,
        article_record['document_id'],
        article_record
    )


def test_delete_document(setup, database_service):
    article_record = get_article_record({'Test': 'Test5'})
    database_service.register(
        article_record['document_id'],
        article_record
    )

    record_check = database_service.read(article_record['document_id'])
    database_service.delete(
        article_record['document_id'],
        record_check
    )
    pytest.raises(DocumentNotFound,
                  database_service.read,
                  article_record['document_id'])


def test_delete_document_not_found(setup, database_service):
    article_record = get_article_record({'Test': 'Test6'})
    pytest.raises(
        DocumentNotFound,
        database_service.delete,
        article_record['document_id'],
        article_record
    )
