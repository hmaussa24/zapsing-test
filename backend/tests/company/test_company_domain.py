import pytest
from modules.company.domain.entities import Company


def test_company_factory_valid():
    c = Company.create('  Acme   Inc  ', '  tok  ')
    assert c.id is None
    assert c.name == 'Acme Inc'
    assert c.api_token == 'tok'


@pytest.mark.parametrize('name', ['', '   '])
def test_company_factory_invalid_name(name):
    with pytest.raises(ValueError):
        Company.create(name, 'tok')


@pytest.mark.parametrize('token', ['', '   '])
def test_company_factory_invalid_token(token):
    with pytest.raises(ValueError):
        Company.create('Acme', token)


def test_company_rename_and_rotate():
    c = Company.create('Acme', 'tok')
    c.rename('  New   Name ')
    assert c.name == 'New Name'
    c.rotate_token(' newtok ')
    assert c.api_token == 'newtok'


