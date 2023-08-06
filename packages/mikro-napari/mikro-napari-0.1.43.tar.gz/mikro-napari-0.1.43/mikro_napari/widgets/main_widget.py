from typing import List
from arkitekt.widgets import SearchWidget
from mikro.structures import (
    Representation,
    Sample,
)
from mikro_napari.api.structures import MultiScaleSample
from mikro_napari.helpers.stage import StageHelper
from arkitekt.messages.postman.provide.bounced_provide import BouncedProvideMessage
from qtpy import QtWidgets
from mikro.widgets import MY_TOP_REPRESENTATIONS, MY_TOP_SAMPLES
from arkitekt.qt.agent import QtAgent
from arkitekt.qt.widgets.magic_bar import MagicBar
from arkitekt.qt.widgets.settings_popup import SettingsPopup
from arkitekt.qt.widgets.provisions import ProvisionsWidget
from arkitekt.qt.widgets.templates import TemplatesWidget
from herre.qt import QtHerre
from fakts.qt import QtFakts
from fakts.grants.qt.qtbeacon import QtSelectableBeaconGrant


class NapariSettings(SettingsPopup):
    def __init__(self, magic_bar, *args, **kwargs):
        super().__init__(magic_bar, *args, **kwargs)
        self.layout.addWidget(ProvisionsWidget(magic_bar.agent))
        self.layout.addWidget(TemplatesWidget(magic_bar.agent))


class NapariMagicBar(MagicBar):
    settingsPopupClass = NapariSettings


SMLM_REPRESENTATIONS = SearchWidget(
    query="""
                    query Search($search: String){
                        options: representations(name: $search, tags: ["smlm"]){
                            value: id
                            label: name
                        }
                    }
                    """
)  #


MULTISCALE_REPRESENTATIONS = SearchWidget(
    query="""
        query Search($search: String){
            options: representations(name: $search, derivedTags: ["multiscale"]){
                value: id
                label: name
            }
        }
        """
)


class ArkitektWidget(QtWidgets.QWidget):
    def __init__(self, napari_viewer, *args, parent=None, **kwargs) -> None:
        super().__init__(*args, **kwargs, parent=parent)

        # Different Grants

        self.beacon_grant = QtSelectableBeaconGrant(parent=self)

        self.fakts = QtFakts(
            grants=[self.beacon_grant],
            subapp="napari",
            hard_fakts={
                "herre": {"client_id": "go8CAE78FDf4eLsOSk4wkR4usYbsamcq0yTYqBiY"}
            },
            parent=self,
        )
        self.herre = QtHerre()

        self.helper = StageHelper(napari_viewer)

        self.magic_bar = NapariMagicBar(
            self.fakts, self.herre, self.agent, parent=self, darkMode=True
        )

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.magic_bar)
        self.setLayout(self.layout)

    def really_show(self, rep: Representation, stream: bool = True):
        """Show Image

        Displays an Image on Napari

        Args:
            rep (Representation): The image you want to display
            stream (bool, optional): Do you want to stream the image or download it?
        """
        return self.helper.open_as_layer(rep)

    def really_show_list(self, reps: List[Representation], stream: bool = True):
        """Show Images

        Displays Images on Napari as a list

        Args:
            reps (Representation): The image you want to display
            stream (bool, optional): Do you want to stream the image or download it?
        """
        print(reps)
        for rep in reps:
            self.helper.open_as_layer(rep)
        return

    def open_locs(self, rep: Representation):
        """Open Localization

        Opens this Image with Localization data displayed

        Args:
            rep (Representation): The image you want to display
        """
        return self.helper.open_with_localizations(rep)

    def open_multiview(self, rep: Representation):
        """Open MultiView

        Opens this Image with multiview

        Args:
            rep (Representation): The image you want to display
        """
        return self.helper.open_multiscale(rep)

    def open_aside(self, reps: List[Representation]):
        """Tile Images

        Opens these images aside from another

        Args:
            rep (Representation): The image you want to display
        """
        return self.helper.open_aside(reps)

    def open_multisample(self, samples: List[Sample], stream=False):
        """Open Samples

        Opens the initial dataset of a sample

        Args:
            samples (List[Sample]): The samples you want to display
        """
        return self.helper.open_multisample(samples, stream=stream)

    def open_sample(self, sample: MultiScaleSample, stream=True):
        """Open Sample

        Opens an sample and tries to marry all of the metadata

        Args:
            sample (Sample): The image you want to display
        """
        return self.helper.open_sample(sample, stream=stream)

    def upload(self, name: str = None, sample: Sample = None) -> Representation:
        """Upload an Active Image

        Uploads the curently active image on Napari

        Args:
            name (str, optional): How do you want to name the image?
            sample (Sample, optional): Which sample should we put the new image in?

        Returns:
            Representation: The uploaded image from the app
        """
        return self.helper.upload_everything(image_name=name, sample=sample)
