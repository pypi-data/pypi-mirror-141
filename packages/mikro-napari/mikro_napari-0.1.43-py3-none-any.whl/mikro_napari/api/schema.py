from pydantic import BaseModel, Field
from mikro.traits import Representation, Sample
from typing import Dict, AsyncIterator, Literal, Optional, Iterator, List
from enum import Enum
from mikro.funcs import execute, asubscribe, aexecute, subscribe
from turms.types.object import GraphQLObject
from mikro.scalars import Store, XArray
from mikro.mikro import Mikro


class OmeroFileType(str, Enum):
    """An enumeration."""

    TIFF = "TIFF"
    "Tiff"
    JPEG = "JPEG"
    "Jpeg"
    MSR = "MSR"
    "MSR File"
    CZI = "CZI"
    "Zeiss Microscopy File"
    UNKNOWN = "UNKNOWN"
    "Unwknon File Format"


class RepresentationVariety(str, Enum):
    """An enumeration."""

    MASK = "MASK"
    "Mask (Value represent Labels)"
    VOXEL = "VOXEL"
    "Voxel (Value represent Intensity)"
    RGB = "RGB"
    "RGB (First three channel represent RGB)"
    UNKNOWN = "UNKNOWN"
    "Unknown"


class RepresentationVarietyInput(str, Enum):
    """Variety expresses the Type of Representation we are dealing with"""

    MASK = "MASK"
    "Mask (Value represent Labels)"
    VOXEL = "VOXEL"
    "Voxel (Value represent Intensity)"
    RGB = "RGB"
    "RGB (First three channel represent RGB)"
    UNKNOWN = "UNKNOWN"
    "Unknown"


class ROIType(str, Enum):
    """An enumeration."""

    ELLIPSE = "ELLIPSE"
    "Ellipse"
    POLYGON = "POLYGON"
    "POLYGON"
    LINE = "LINE"
    "Line"
    RECTANGLE = "RECTANGLE"
    "Rectangle"
    PATH = "PATH"
    "Path"
    UNKNOWN = "UNKNOWN"
    "Unknown"


class RoiTypeInput(str, Enum):
    """An enumeration."""

    ELLIPSIS = "ELLIPSIS"
    "Ellipse"
    POLYGON = "POLYGON"
    "POLYGON"
    LINE = "LINE"
    "Line"
    RECTANGLE = "RECTANGLE"
    "Rectangle"
    PATH = "PATH"
    "Path"
    UNKNOWN = "UNKNOWN"
    "Unknown"


class OmeroRepresentationInput(BaseModel):
    planes: Optional[List[Optional["PlaneInput"]]]
    channels: Optional[List[Optional["ChannelInput"]]]
    physicalSize: Optional["PhysicalSizeInput"]
    scale: Optional[List[Optional[float]]]


class PlaneInput(BaseModel):
    zIndex: Optional[int]
    yIndex: Optional[int]
    xIndex: Optional[int]
    cIndex: Optional[int]
    tIndex: Optional[int]
    exposureTime: Optional[float]
    deltaT: Optional[float]


class ChannelInput(BaseModel):
    name: Optional[str]
    emmissionWavelength: Optional[float]
    excitationWavelength: Optional[float]
    acquisitionMode: Optional[str]
    color: Optional[str]


class PhysicalSizeInput(BaseModel):
    x: Optional[int]
    y: Optional[int]
    z: Optional[int]
    t: Optional[int]
    c: Optional[int]


class InputVector(BaseModel):
    x: Optional[float]
    "X-coordinate"
    y: Optional[float]
    "Y-coordinate"
    z: Optional[float]
    "Z-coordinate"


OmeroRepresentationInput.update_forward_refs()


class MultiScaleRepresentationFragmentDerived(Representation, GraphQLObject):
    """A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest"""

    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    name: Optional[str]
    "Cleartext name"
    tags: Optional[List[Optional[str]]]
    "A comma-separated list of tags."
    meta: Optional[Dict]
    store: Optional[Store]

    class Config:
        frozen = True


class MultiScaleRepresentationFragment(Representation, GraphQLObject):
    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    derived: Optional[List[Optional[MultiScaleRepresentationFragmentDerived]]]
    "Derived Images from this Image"

    class Config:
        frozen = True


class RepresentationFragmentSample(Sample, GraphQLObject):
    """Samples are storage containers for representations. A Sample is to be understood analogous to a Biological Sample. It existed in Time (the time of acquisiton and experimental procedure),
    was measured in space (x,y,z) and in different modalities (c). Sample therefore provide a datacontainer where each Representation of
    the data shares the same dimensions. Every transaction to our image data is still part of the original acuqistion, so also filtered images are refering back to the sample
    """

    typename: Optional[Literal["Sample"]] = Field(alias="__typename")
    name: str

    class Config:
        frozen = True


class RepresentationFragment(Representation, GraphQLObject):
    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    sample: Optional[RepresentationFragmentSample]
    "The Sample this representation belongs to"
    type: Optional[str]
    "The Representation can have varying types, consult your API"
    id: str
    store: Optional[Store]
    variety: RepresentationVariety
    "The Representation can have varying types, consult your API"
    name: Optional[str]
    "Cleartext name"

    class Config:
        frozen = True


class ListRepresentationFragmentSample(Sample, GraphQLObject):
    """Samples are storage containers for representations. A Sample is to be understood analogous to a Biological Sample. It existed in Time (the time of acquisiton and experimental procedure),
    was measured in space (x,y,z) and in different modalities (c). Sample therefore provide a datacontainer where each Representation of
    the data shares the same dimensions. Every transaction to our image data is still part of the original acuqistion, so also filtered images are refering back to the sample
    """

    typename: Optional[Literal["Sample"]] = Field(alias="__typename")
    name: str

    class Config:
        frozen = True


class ListRepresentationFragment(Representation, GraphQLObject):
    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    id: str
    name: Optional[str]
    "Cleartext name"
    sample: Optional[ListRepresentationFragmentSample]
    "The Sample this representation belongs to"

    class Config:
        frozen = True


class ROIFragmentVectors(GraphQLObject):
    typename: Optional[Literal["Vector"]] = Field(alias="__typename")
    x: Optional[float]
    "X-coordinate"
    y: Optional[float]
    "Y-coordinate"
    z: Optional[float]
    "Z-coordinate"

    class Config:
        frozen = True


class ROIFragmentRepresentation(Representation, GraphQLObject):
    """A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest"""

    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    id: str

    class Config:
        frozen = True


class ROIFragmentCreator(GraphQLObject):
    """A reflection on the real User"""

    typename: Optional[Literal["User"]] = Field(alias="__typename")
    id: str

    class Config:
        frozen = True


class ROIFragment(GraphQLObject):
    typename: Optional[Literal["ROI"]] = Field(alias="__typename")
    id: str
    vectors: Optional[List[Optional[ROIFragmentVectors]]]
    type: ROIType
    "The Representation can have varying types, consult your API"
    representation: Optional[ROIFragmentRepresentation]
    creator: ROIFragmentCreator

    class Config:
        frozen = True


class MultiScaleSampleFragmentRepresentationsDerived(Representation, GraphQLObject):
    """A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest"""

    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    store: Optional[Store]

    class Config:
        frozen = True


class MultiScaleSampleFragmentRepresentations(Representation, GraphQLObject):
    """A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest"""

    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    id: str
    store: Optional[Store]
    derived: Optional[List[Optional[MultiScaleSampleFragmentRepresentationsDerived]]]
    "Derived Images from this Image"

    class Config:
        frozen = True


class MultiScaleSampleFragment(Sample, GraphQLObject):
    typename: Optional[Literal["Sample"]] = Field(alias="__typename")
    id: str
    name: str
    representations: Optional[List[Optional[MultiScaleSampleFragmentRepresentations]]]

    class Config:
        frozen = True


class Get_multiscale_repQuery(GraphQLObject):
    representation: Optional[MultiScaleRepresentationFragment]

    class Meta:
        domain = "napari"
        document = 'fragment MultiScaleRepresentation on Representation {\n  derived(tags: ["multiscale"]) {\n    name\n    tags\n    meta\n    store\n  }\n}\n\nquery get_multiscale_rep($id: ID!) {\n  representation(id: $id) {\n    ...MultiScaleRepresentation\n  }\n}'

    class Config:
        frozen = True


class Get_representationQuery(GraphQLObject):
    representation: Optional[RepresentationFragment]

    class Meta:
        domain = "napari"
        document = "fragment Representation on Representation {\n  sample {\n    name\n  }\n  type\n  id\n  store\n  variety\n  name\n}\n\nquery get_representation($id: ID!) {\n  representation(id: $id) {\n    ...Representation\n  }\n}"

    class Config:
        frozen = True


class Get_some_representationsQuery(GraphQLObject):
    representations: Optional[List[Optional[ListRepresentationFragment]]]

    class Meta:
        domain = "napari"
        document = 'fragment ListRepresentation on Representation {\n  id\n  name\n  sample {\n    name\n  }\n}\n\nquery get_some_representations {\n  representations(limit: 10, order: "-created_at") {\n    ...ListRepresentation\n  }\n}'

    class Config:
        frozen = True


class Get_roisQuery(GraphQLObject):
    rois: Optional[List[Optional[ROIFragment]]]

    class Meta:
        domain = "napari"
        document = "fragment ROI on ROI {\n  id\n  vectors {\n    x\n    y\n    z\n  }\n  type\n  representation {\n    id\n  }\n  creator {\n    id\n  }\n}\n\nquery get_rois($representation: ID!, $type: [RoiTypeInput]) {\n  rois(representation: $representation, type: $type) {\n    ...ROI\n  }\n}"

    class Config:
        frozen = True


class Expand_multiscaleQuery(GraphQLObject):
    sample: Optional[MultiScaleSampleFragment]

    class Meta:
        domain = "napari"
        document = 'fragment MultiScaleSample on Sample {\n  id\n  name\n  representations(tags: ["multiscale"]) {\n    id\n    store\n    derived(ordering: "-meta_multiscale_depth") {\n      store\n    }\n  }\n}\n\nquery expand_multiscale($id: ID!) {\n  sample(id: $id) {\n    ...MultiScaleSample\n  }\n}'

    class Config:
        frozen = True


class Watch_roisSubscriptionRois(GraphQLObject):
    typename: Optional[Literal["RoiEvent"]] = Field(alias="__typename")
    update: Optional[ROIFragment]
    delete: Optional[str]
    create: Optional[ROIFragment]

    class Config:
        frozen = True


class Watch_roisSubscription(GraphQLObject):
    rois: Optional[Watch_roisSubscriptionRois]

    class Meta:
        domain = "napari"
        document = "fragment ROI on ROI {\n  id\n  vectors {\n    x\n    y\n    z\n  }\n  type\n  representation {\n    id\n  }\n  creator {\n    id\n  }\n}\n\nsubscription watch_rois($representation: ID!) {\n  rois(representation: $representation) {\n    update {\n      ...ROI\n    }\n    delete\n    create {\n      ...ROI\n    }\n  }\n}"

    class Config:
        frozen = True


class Create_roiMutation(GraphQLObject):
    createROI: Optional[ROIFragment]

    class Meta:
        domain = "napari"
        document = "fragment ROI on ROI {\n  id\n  vectors {\n    x\n    y\n    z\n  }\n  type\n  representation {\n    id\n  }\n  creator {\n    id\n  }\n}\n\nmutation create_roi($representation: ID!, $vectors: [InputVector]!, $creator: ID, $type: RoiTypeInput) {\n  createROI(\n    representation: $representation\n    vectors: $vectors\n    type: $type\n    creator: $creator\n  ) {\n    ...ROI\n  }\n}"

    class Config:
        frozen = True


class Delete_roiMutationDeleteroi(GraphQLObject):
    typename: Optional[Literal["DeleteROIResult"]] = Field(alias="__typename")
    id: Optional[str]

    class Config:
        frozen = True


class Delete_roiMutation(GraphQLObject):
    deleteROI: Optional[Delete_roiMutationDeleteroi]

    class Meta:
        domain = "napari"
        document = (
            "mutation delete_roi($id: ID!) {\n  deleteROI(id: $id) {\n    id\n  }\n}"
        )

    class Config:
        frozen = True


class Create_imageMutationImage1Derived(Representation, GraphQLObject):
    """A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest"""

    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    id: str

    class Config:
        frozen = True


class Create_imageMutationImage1(Representation, GraphQLObject):
    """A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest"""

    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    id: str
    name: Optional[str]
    "Cleartext name"
    derived: Optional[List[Optional[Create_imageMutationImage1Derived]]]
    "Derived Images from this Image"

    class Config:
        frozen = True


class Create_imageMutationImage2Derived(Representation, GraphQLObject):
    """A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest"""

    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    id: str

    class Config:
        frozen = True


class Create_imageMutationImage2(Representation, GraphQLObject):
    """A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest"""

    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    id: str
    name: Optional[str]
    "Cleartext name"
    derived: Optional[List[Optional[Create_imageMutationImage2Derived]]]
    "Derived Images from this Image"

    class Config:
        frozen = True


class Create_imageMutation(GraphQLObject):
    image1: Optional[Create_imageMutationImage1]
    image2: Optional[Create_imageMutationImage2]

    class Meta:
        domain = "napari"
        document = "mutation create_image($xarray: XArray!) {\n  image1: fromXArray(xarray: $xarray) {\n    id\n    name\n    derived {\n      id\n    }\n  }\n  image2: fromXArray(xarray: $xarray) {\n    id\n    name\n    derived {\n      id\n    }\n  }\n}"

    class Config:
        frozen = True


async def aget_multiscale_rep(
    id: str, mikro: Mikro = None
) -> MultiScaleRepresentationFragment:
    """get_multiscale_rep

    Get a single representation by ID

    Arguments:
        id (ID): ID
        mikro (mikro.mikro.Mikro): The mikro client

    Returns:
        MultiScaleRepresentationFragment: The returned Mutation"""
    return (
        await aexecute(Get_multiscale_repQuery, {"id": id}, mikro=mikro)
    ).representation


def get_multiscale_rep(
    id: str, mikro: Mikro = None
) -> MultiScaleRepresentationFragment:
    """get_multiscale_rep

    Get a single representation by ID

    Arguments:
        id (ID): ID
        mikro (mikro.mikro.Mikro): The mikro client

    Returns:
        MultiScaleRepresentationFragment: The returned Mutation"""
    return execute(Get_multiscale_repQuery, {"id": id}, mikro=mikro).representation


async def aget_representation(id: str, mikro: Mikro = None) -> RepresentationFragment:
    """get_representation

    Get a single representation by ID

    Arguments:
        id (ID): ID
        mikro (mikro.mikro.Mikro): The mikro client

    Returns:
        RepresentationFragment: The returned Mutation"""
    return (
        await aexecute(Get_representationQuery, {"id": id}, mikro=mikro)
    ).representation


def get_representation(id: str, mikro: Mikro = None) -> RepresentationFragment:
    """get_representation

    Get a single representation by ID

    Arguments:
        id (ID): ID
        mikro (mikro.mikro.Mikro): The mikro client

    Returns:
        RepresentationFragment: The returned Mutation"""
    return execute(Get_representationQuery, {"id": id}, mikro=mikro).representation


async def aget_some_representations(
    mikro: Mikro = None,
) -> List[ListRepresentationFragment]:
    """get_some_representations

    All represetations

    Arguments:
        mikro (mikro.mikro.Mikro): The mikro client

    Returns:
        ListRepresentationFragment: The returned Mutation"""
    return (
        await aexecute(Get_some_representationsQuery, {}, mikro=mikro)
    ).representations


def get_some_representations(mikro: Mikro = None) -> List[ListRepresentationFragment]:
    """get_some_representations

    All represetations

    Arguments:
        mikro (mikro.mikro.Mikro): The mikro client

    Returns:
        ListRepresentationFragment: The returned Mutation"""
    return execute(Get_some_representationsQuery, {}, mikro=mikro).representations


async def aget_rois(
    representation: str, type: List[RoiTypeInput] = None, mikro: Mikro = None
) -> List[ROIFragment]:
    """get_rois

    All represetations

    Arguments:
        representation (ID): ID
        type (List[RoiTypeInput], Optional): RoiTypeInput
        mikro (mikro.mikro.Mikro): The mikro client

    Returns:
        ROIFragment: The returned Mutation"""
    return (
        await aexecute(
            Get_roisQuery, {"representation": representation, "type": type}, mikro=mikro
        )
    ).rois


def get_rois(
    representation: str, type: List[RoiTypeInput] = None, mikro: Mikro = None
) -> List[ROIFragment]:
    """get_rois

    All represetations

    Arguments:
        representation (ID): ID
        type (List[RoiTypeInput], Optional): RoiTypeInput
        mikro (mikro.mikro.Mikro): The mikro client

    Returns:
        ROIFragment: The returned Mutation"""
    return execute(
        Get_roisQuery, {"representation": representation, "type": type}, mikro=mikro
    ).rois


async def aexpand_multiscale(id: str, mikro: Mikro = None) -> MultiScaleSampleFragment:
    """expand_multiscale

    Get a single representation by ID

    Arguments:
        id (ID): ID
        mikro (mikro.mikro.Mikro): The mikro client

    Returns:
        MultiScaleSampleFragment: The returned Mutation"""
    return (await aexecute(Expand_multiscaleQuery, {"id": id}, mikro=mikro)).sample


def expand_multiscale(id: str, mikro: Mikro = None) -> MultiScaleSampleFragment:
    """expand_multiscale

    Get a single representation by ID

    Arguments:
        id (ID): ID
        mikro (mikro.mikro.Mikro): The mikro client

    Returns:
        MultiScaleSampleFragment: The returned Mutation"""
    return execute(Expand_multiscaleQuery, {"id": id}, mikro=mikro).sample


async def awatch_rois(
    representation: str, mikro: Mikro = None
) -> AsyncIterator[Watch_roisSubscriptionRois]:
    """watch_rois



    Arguments:
        representation (ID): ID
        mikro (mikro.mikro.Mikro): The mikro client

    Returns:
        Watch_roisSubscriptionRois: The returned Mutation"""
    async for event in asubscribe(
        Watch_roisSubscription, {"representation": representation}, mikro=mikro
    ):
        yield event.rois


def watch_rois(
    representation: str, mikro: Mikro = None
) -> Iterator[Watch_roisSubscriptionRois]:
    """watch_rois



    Arguments:
        representation (ID): ID
        mikro (mikro.mikro.Mikro): The mikro client

    Returns:
        Watch_roisSubscriptionRois: The returned Mutation"""
    for event in subscribe(
        Watch_roisSubscription, {"representation": representation}, mikro=mikro
    ):
        yield event.rois


async def acreate_roi(
    representation: str,
    vectors: List[InputVector],
    creator: str = None,
    type: RoiTypeInput = None,
    mikro: Mikro = None,
) -> ROIFragment:
    """create_roi

    Creates a Sample

    Arguments:
        representation (ID): ID
        vectors (List[InputVector]): InputVector
        creator (ID, Optional): ID
        type (RoiTypeInput, Optional): RoiTypeInput
        mikro (mikro.mikro.Mikro): The mikro client

    Returns:
        ROIFragment: The returned Mutation"""
    return (
        await aexecute(
            Create_roiMutation,
            {
                "representation": representation,
                "vectors": vectors,
                "creator": creator,
                "type": type,
            },
            mikro=mikro,
        )
    ).createROI


def create_roi(
    representation: str,
    vectors: List[InputVector],
    creator: str = None,
    type: RoiTypeInput = None,
    mikro: Mikro = None,
) -> ROIFragment:
    """create_roi

    Creates a Sample

    Arguments:
        representation (ID): ID
        vectors (List[InputVector]): InputVector
        creator (ID, Optional): ID
        type (RoiTypeInput, Optional): RoiTypeInput
        mikro (mikro.mikro.Mikro): The mikro client

    Returns:
        ROIFragment: The returned Mutation"""
    return execute(
        Create_roiMutation,
        {
            "representation": representation,
            "vectors": vectors,
            "creator": creator,
            "type": type,
        },
        mikro=mikro,
    ).createROI


async def adelete_roi(id: str, mikro: Mikro = None) -> Delete_roiMutationDeleteroi:
    """delete_roi

    Create an experiment (only signed in users)

    Arguments:
        id (ID): ID
        mikro (mikro.mikro.Mikro): The mikro client

    Returns:
        Delete_roiMutationDeleteroi: The returned Mutation"""
    return (await aexecute(Delete_roiMutation, {"id": id}, mikro=mikro)).deleteROI


def delete_roi(id: str, mikro: Mikro = None) -> Delete_roiMutationDeleteroi:
    """delete_roi

    Create an experiment (only signed in users)

    Arguments:
        id (ID): ID
        mikro (mikro.mikro.Mikro): The mikro client

    Returns:
        Delete_roiMutationDeleteroi: The returned Mutation"""
    return execute(Delete_roiMutation, {"id": id}, mikro=mikro).deleteROI


async def acreate_image(xarray: XArray, mikro: Mikro = None) -> Create_imageMutation:
    """create_image


     image1: Creates a Representation
     image2: Creates a Representation

    Arguments:
        xarray (XArray): XArray
        mikro (mikro.mikro.Mikro): The mikro client

    Returns:
        Create_imageMutation: The returned Mutation"""
    return await aexecute(Create_imageMutation, {"xarray": xarray}, mikro=mikro)


def create_image(xarray: XArray, mikro: Mikro = None) -> Create_imageMutation:
    """create_image


     image1: Creates a Representation
     image2: Creates a Representation

    Arguments:
        xarray (XArray): XArray
        mikro (mikro.mikro.Mikro): The mikro client

    Returns:
        Create_imageMutation: The returned Mutation"""
    return execute(Create_imageMutation, {"xarray": xarray}, mikro=mikro)
