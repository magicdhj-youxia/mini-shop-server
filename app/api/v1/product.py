# _*_ coding: utf-8 _*_
"""
  Created by Allen7D on 2018/6/17.
  ↓↓↓ 产品接口 ↓↓↓
"""
from app.libs.error_code import Success
from app.libs.redprint import RedPrint
from app.libs.token_auth import auth
from app.models.product import Product
from app.validators.forms import PaginateValidator, CountValidator, IDMustBePositiveIntValidator
from app.api_docs.v1 import product as api_doc

__author__ = 'Allen7D'

api = RedPrint(name='product', description='产品', api_doc=api_doc)


@api.route('/recent', methods=['GET'])
@api.doc(args=['count'])
def get_recent():
    '''最新的商品'''
    count = CountValidator.validate_for_api().count.data
    product_list = Product.get_most_recent(count=count)
    return Success(product_list)


@api.route('/all/by_category', methods=['GET'])
@api.doc(args=['g.query.category_id'])
def get_all_by_category():
    '''所有 category_id 类的商品'''
    id = IDMustBePositiveIntValidator().validate_for_api().id.data
    product_list = Product.get_product_by_category(id=id)
    return Success(product_list)


@api.route('/list/by_category', methods=['GET'])
@api.doc(args=['g.query.page', 'g.query.size', 'g.query.category_id'], auth=True)
@auth.login_required
def get_list_by_category():
    '''获取商品列表(分页&基于categoryID)'''
    id = IDMustBePositiveIntValidator().validate_for_api().id.data
    page_validator = PaginateValidator().validate_for_api()
    page = page_validator.page.data
    size = page_validator.size.data

    paginator = Product.query.filter_by(category_id=id).paginate(page=page, per_page=size, error_out=False)
    return Success({
        'total': paginator.total,
        'current_page': paginator.page,
        'items': paginator.items
    })


@api.route('/<int:id>', methods=['GET'])
@api.doc(args=['g.path.product_id'])
def get_product(id):
    '''获取某商品信息'''
    product = Product.get_product_detail(id=id)
    return Success(product)


@api.route('/<int:id>', methods=['POST'])
@api.route_meta(auth='新增商品', module='商品')
@api.doc(args=['g.path.product_id'], auth=True)
@auth.group_required
def create_product(id):
    '''新增商品'''
    return Success(error_code=1)


@api.route('/<int:id>', methods=['PUT'])
@api.route_meta(auth='更新商品', module='商品')
@api.doc(args=['g.path.product_id'], auth=True)
@auth.group_required
def update_product(id):
    '''更新商品'''
    return Success(error_code=1)


@api.route('/<int:id>', methods=['DELETE'])
@api.route_meta(auth='删除商品', module='商品')
@api.doc(args=['g.path.product_id'], auth=True)
@auth.group_required
def delete_product(id):
    '''删除商品'''
    product = Product.get_or_404(id=id)
    product.delete()
    return Success(error_code=2)
