'''
# replace this
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_stepfunctions
import constructs


@jsii.interface(jsii_type="schadem-cdk-construct-test1.IIsomeProps")
class IIsomeProps(typing_extensions.Protocol):
    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="someProps")
    def some_props(self) -> builtins.str:
        ...

    @some_props.setter
    def some_props(self, value: builtins.str) -> None:
        ...


class _IIsomePropsProxy:
    __jsii_type__: typing.ClassVar[str] = "schadem-cdk-construct-test1.IIsomeProps"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="someProps")
    def some_props(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "someProps"))

    @some_props.setter
    def some_props(self, value: builtins.str) -> None:
        jsii.set(self, "someProps", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IIsomeProps).__jsii_proxy_class__ = lambda : _IIsomePropsProxy


class MyWorkFlowChain(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="schadem-cdk-construct-test1.MyWorkFlowChain",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        workflow_chain: aws_cdk.aws_stepfunctions.Chain,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param workflow_chain: -
        '''
        jsii.create(self.__class__, self, [scope, id, workflow_chain])


__all__ = [
    "IIsomeProps",
    "MyWorkFlowChain",
]

publication.publish()
