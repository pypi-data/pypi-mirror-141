"""Menu items for the Lifecycle Management plugin."""
# pylint: disable=C0412
from nautobot.utilities.choices import ButtonColorChoices

try:
    from nautobot.core.apps import NavMenuTab, NavMenuGroup, NavMenuItem, NavMenuButton

    menu_items = (
        NavMenuTab(
            name="Device Lifecycle",
            weight=600,
            groups=(
                NavMenuGroup(
                    name="Hardware Notices",
                    weight=100,
                    items=(
                        NavMenuItem(
                            link="plugins:nautobot_device_lifecycle_mgmt:hardwarelcm_list",
                            name="Hardware Notices",
                            buttons=(
                                NavMenuButton(
                                    link="plugins:nautobot_device_lifecycle_mgmt:hardwarelcm_add",
                                    title="Add",
                                    icon_class="mdi mdi-plus-thick",
                                    button_class=ButtonColorChoices.GREEN,
                                    permissions=[
                                        "nautobot_device_lifecycle_mgmt.add_hardwarelcm",
                                    ],
                                ),
                                NavMenuButton(
                                    link="plugins:nautobot_device_lifecycle_mgmt:hardwarelcm_import",
                                    title="Import",
                                    icon_class="mdi mdi-database-import-outline",
                                    button_class=ButtonColorChoices.BLUE,
                                    permissions=[
                                        "nautobot_device_lifecycle_mgmt.add_hardwarelcm",
                                    ],
                                ),
                            ),
                            permissions=[
                                "nautobot_device_lifecycle_mgmt.view_hardwarelcm",
                            ],
                        ),
                    ),
                ),
                NavMenuGroup(
                    name="Software Lifecycle",
                    weight=100,
                    items=(
                        NavMenuItem(
                            link="plugins:nautobot_device_lifecycle_mgmt:softwarelcm_list",
                            name="Software",
                            buttons=(
                                NavMenuButton(
                                    link="plugins:nautobot_device_lifecycle_mgmt:softwarelcm_add",
                                    title="Add",
                                    icon_class="mdi mdi-plus-thick",
                                    button_class=ButtonColorChoices.GREEN,
                                    permissions=[
                                        "nautobot_device_lifecycle_mgmt.add_softwarelcm",
                                    ],
                                ),
                                NavMenuButton(
                                    link="plugins:nautobot_device_lifecycle_mgmt:softwarelcm_import",
                                    title="Import",
                                    icon_class="mdi mdi-database-import-outline",
                                    button_class=ButtonColorChoices.BLUE,
                                    permissions=["nautobot_device_lifecycle_mgmt.add_softwarelcm"],
                                ),
                            ),
                            permissions=[
                                "nautobot_device_lifecycle_mgmt.view_softwarelcm",
                            ],
                        ),
                        NavMenuItem(
                            link="plugins:nautobot_device_lifecycle_mgmt:softwareimagelcm_list",
                            name="Software Image",
                            buttons=(
                                NavMenuButton(
                                    link="plugins:nautobot_device_lifecycle_mgmt:softwareimagelcm_add",
                                    title="Add",
                                    icon_class="mdi mdi-plus-thick",
                                    button_class=ButtonColorChoices.GREEN,
                                    permissions=[
                                        "nautobot_device_lifecycle_mgmt.add_softwareimagelcm",
                                    ],
                                ),
                                NavMenuButton(
                                    link="plugins:nautobot_device_lifecycle_mgmt:softwareimagelcm_import",
                                    title="Import",
                                    icon_class="mdi mdi-database-import-outline",
                                    button_class=ButtonColorChoices.BLUE,
                                    permissions=["nautobot_device_lifecycle_mgmt.add_softwareimagelcm"],
                                ),
                            ),
                            permissions=[
                                "nautobot_device_lifecycle_mgmt.view_softwareimagelcm",
                            ],
                        ),
                        NavMenuItem(
                            link="plugins:nautobot_device_lifecycle_mgmt:validatedsoftwarelcm_list",
                            name="Validated Software",
                            buttons=(
                                NavMenuButton(
                                    link="plugins:nautobot_device_lifecycle_mgmt:validatedsoftwarelcm_add",
                                    title="Add",
                                    icon_class="mdi mdi-plus-thick",
                                    button_class=ButtonColorChoices.GREEN,
                                    permissions=[
                                        "nautobot_device_lifecycle_mgmt.add_validatedsoftwarelcm",
                                    ],
                                ),
                                NavMenuButton(
                                    link="plugins:nautobot_device_lifecycle_mgmt:validatedsoftwarelcm_import",
                                    title="Import",
                                    icon_class="mdi mdi-database-import-outline",
                                    button_class=ButtonColorChoices.BLUE,
                                    permissions=["nautobot_device_lifecycle_mgmt.add_validatedsoftwarelcm"],
                                ),
                            ),
                            permissions=[
                                "nautobot_device_lifecycle_mgmt.view_validatedsoftwarelcm",
                            ],
                        ),
                        NavMenuItem(
                            link="plugins:nautobot_device_lifecycle_mgmt:cvelcm_list",
                            name="CVE",
                            buttons=(
                                NavMenuButton(
                                    link="plugins:nautobot_device_lifecycle_mgmt:cvelcm_add",
                                    title="Add",
                                    icon_class="mdi mdi-plus-thick",
                                    button_class=ButtonColorChoices.GREEN,
                                    permissions=[
                                        "nautobot_device_lifecycle_mgmt.add_cvelcm",
                                    ],
                                ),
                                NavMenuButton(
                                    link="plugins:nautobot_device_lifecycle_mgmt:cvelcm_import",
                                    title="Import",
                                    icon_class="mdi mdi-database-import-outline",
                                    button_class=ButtonColorChoices.BLUE,
                                    permissions=["nautobot_device_lifecycle_mgmt.add_cvelcm"],
                                ),
                            ),
                            permissions=[
                                "nautobot_device_lifecycle_mgmt.view_cvelcm",
                            ],
                        ),
                        NavMenuItem(
                            link="plugins:nautobot_device_lifecycle_mgmt:vulnerabilitylcm_list",
                            name="Vulnerability",
                            permissions=[
                                "nautobot_device_lifecycle_mgmt.view_vulnerabilitylcm",
                            ],
                        ),
                    ),
                ),
                NavMenuGroup(
                    name="Contracts",
                    weight=100,
                    items=(
                        NavMenuItem(
                            link="plugins:nautobot_device_lifecycle_mgmt:contractlcm_list",
                            name="Contracts",
                            buttons=(
                                NavMenuButton(
                                    link="plugins:nautobot_device_lifecycle_mgmt:contractlcm_add",
                                    title="Add",
                                    icon_class="mdi mdi-plus-thick",
                                    button_class=ButtonColorChoices.GREEN,
                                    permissions=[
                                        "nautobot_device_lifecycle_mgmt.add_contractlcm",
                                    ],
                                ),
                                NavMenuButton(
                                    link="plugins:nautobot_device_lifecycle_mgmt:contractlcm_import",
                                    title="Import",
                                    icon_class="mdi mdi-database-import-outline",
                                    button_class=ButtonColorChoices.BLUE,
                                    permissions=[
                                        "nautobot_device_lifecycle_mgmt.add_contractlcm",
                                    ],
                                ),
                            ),
                            permissions=[
                                "nautobot_device_lifecycle_mgmt.view_contractlcm",
                            ],
                        ),
                        NavMenuItem(
                            link="plugins:nautobot_device_lifecycle_mgmt:providerlcm_list",
                            name="Vendors",
                            buttons=(
                                NavMenuButton(
                                    link="plugins:nautobot_device_lifecycle_mgmt:providerlcm_add",
                                    title="Add",
                                    icon_class="mdi mdi-plus-thick",
                                    button_class=ButtonColorChoices.GREEN,
                                    permissions=[
                                        "nautobot_device_lifecycle_mgmt.add_providerlcm",
                                    ],
                                ),
                                NavMenuButton(
                                    link="plugins:nautobot_device_lifecycle_mgmt:providerlcm_import",
                                    title="Import",
                                    icon_class="mdi mdi-database-import-outline",
                                    button_class=ButtonColorChoices.BLUE,
                                    permissions=[
                                        "nautobot_device_lifecycle_mgmt.add_providerlcm",
                                    ],
                                ),
                            ),
                            permissions=[
                                "nautobot_device_lifecycle_mgmt.view_providerlcm",
                            ],
                        ),
                        NavMenuItem(
                            link="plugins:nautobot_device_lifecycle_mgmt:contactlcm_list",
                            name="POC",
                            buttons=(
                                NavMenuButton(
                                    link="plugins:nautobot_device_lifecycle_mgmt:contactlcm_add",
                                    title="Add",
                                    icon_class="mdi mdi-plus-thick",
                                    button_class=ButtonColorChoices.GREEN,
                                    permissions=[
                                        "nautobot_device_lifecycle_mgmt.add_contactlcm",
                                    ],
                                ),
                                NavMenuButton(
                                    link="plugins:nautobot_device_lifecycle_mgmt:contactlcm_import",
                                    title="Import",
                                    icon_class="mdi mdi-database-import-outline",
                                    button_class=ButtonColorChoices.BLUE,
                                    permissions=[
                                        "nautobot_device_lifecycle_mgmt.add_contactlcm",
                                    ],
                                ),
                            ),
                            permissions=[
                                "nautobot_device_lifecycle_mgmt.view_contactlcm",
                            ],
                        ),
                    ),
                ),
                NavMenuGroup(
                    name="Reports",
                    weight=100,
                    items=(
                        NavMenuItem(
                            link="plugins:nautobot_device_lifecycle_mgmt:validatedsoftware_device_report",
                            name="Device Software Validation",
                            permissions=[
                                "nautobot_device_lifecycle_mgmt.view_validatedsoftwarelcm",
                            ],
                        ),
                        NavMenuItem(
                            link="plugins:nautobot_device_lifecycle_mgmt:validatedsoftware_inventoryitem_report",
                            name="Inventory Item Software Validation",
                            permissions=[
                                "nautobot_device_lifecycle_mgmt.view_validatedsoftwarelcm",
                            ],
                        ),
                    ),
                ),
            ),
        ),
    )
except ModuleNotFoundError:
    from nautobot.extras.plugins import PluginMenuItem, PluginMenuButton

    menu_items = (
        PluginMenuItem(
            link="plugins:nautobot_device_lifecycle_mgmt:hardwarelcm_list",
            link_text="Hardware Notices",
            buttons=(
                PluginMenuButton(
                    link="plugins:nautobot_device_lifecycle_mgmt:hardwarelcm_add",
                    title="Add",
                    icon_class="mdi mdi-plus-thick",
                    color=ButtonColorChoices.GREEN,
                    permissions=["nautobot_device_lifecycle_mgmt.add_hardwarelcm"],
                ),
                PluginMenuButton(
                    link="plugins:nautobot_device_lifecycle_mgmt:hardwarelcm_import",
                    title="Import",
                    icon_class="mdi mdi-database-import-outline",
                    color=ButtonColorChoices.BLUE,
                    permissions=["nautobot_device_lifecycle_mgmt.add_hardwarelcm"],
                ),
            ),
        ),
        PluginMenuItem(
            link="plugins:nautobot_device_lifecycle_mgmt:contractlcm_list",
            link_text="Contracts",
            buttons=(
                PluginMenuButton(
                    link="plugins:nautobot_device_lifecycle_mgmt:contractlcm_add",
                    title="Add",
                    icon_class="mdi mdi-plus-thick",
                    color=ButtonColorChoices.GREEN,
                    permissions=["nautobot_device_lifecycle_mgmt.add_contractlcm"],
                ),
                PluginMenuButton(
                    link="plugins:nautobot_device_lifecycle_mgmt:contractlcm_import",
                    title="Import",
                    icon_class="mdi mdi-database-import-outline",
                    color=ButtonColorChoices.BLUE,
                    permissions=["nautobot_device_lifecycle_mgmt.add_contractlcm"],
                ),
            ),
        ),
        PluginMenuItem(
            link="plugins:nautobot_device_lifecycle_mgmt:providerlcm_list",
            link_text="Vendors",
            buttons=(
                PluginMenuButton(
                    link="plugins:nautobot_device_lifecycle_mgmt:providerlcm_add",
                    title="Add",
                    icon_class="mdi mdi-plus-thick",
                    color=ButtonColorChoices.GREEN,
                    permissions=["nautobot_device_lifecycle_mgmt.add_providerlcm"],
                ),
                PluginMenuButton(
                    link="plugins:nautobot_device_lifecycle_mgmt:providerlcm_import",
                    title="Import",
                    icon_class="mdi mdi-database-import-outline",
                    color=ButtonColorChoices.BLUE,
                    permissions=["nautobot_device_lifecycle_mgmt.add_providerlcm"],
                ),
            ),
        ),
        PluginMenuItem(
            link="plugins:nautobot_device_lifecycle_mgmt:contactlcm_list",
            link_text="POC",
            buttons=(
                PluginMenuButton(
                    link="plugins:nautobot_device_lifecycle_mgmt:contactlcm_add",
                    title="Add",
                    icon_class="mdi mdi-plus-thick",
                    color=ButtonColorChoices.GREEN,
                    permissions=["nautobot_device_lifecycle_mgmt.add_contactlcm"],
                ),
                PluginMenuButton(
                    link="plugins:nautobot_device_lifecycle_mgmt:contactlcm_import",
                    title="Import",
                    icon_class="mdi mdi-database-import-outline",
                    color=ButtonColorChoices.BLUE,
                    permissions=["nautobot_device_lifecycle_mgmt.add_contactlcm"],
                ),
            ),
        ),
        PluginMenuItem(
            link="plugins:nautobot_device_lifecycle_mgmt:softwarelcm_list",
            link_text="Software",
            buttons=(
                PluginMenuButton(
                    link="plugins:nautobot_device_lifecycle_mgmt:softwarelcm_add",
                    title="Add",
                    icon_class="mdi mdi-plus-thick",
                    color=ButtonColorChoices.GREEN,
                    permissions=["nautobot_device_lifecycle_mgmt.add_softwarelcm"],
                ),
                PluginMenuButton(
                    link="plugins:nautobot_device_lifecycle_mgmt:softwarelcm_import",
                    title="Import",
                    icon_class="mdi mdi-database-import-outline",
                    color=ButtonColorChoices.BLUE,
                    permissions=["nautobot_device_lifecycle_mgmt.add_softwarelcm"],
                ),
            ),
        ),
        PluginMenuItem(
            link="plugins:nautobot_device_lifecycle_mgmt:softwareimagelcm_list",
            link_text="Software Image",
            buttons=(
                PluginMenuButton(
                    link="plugins:nautobot_device_lifecycle_mgmt:softwareimagelcm_add",
                    title="Add",
                    icon_class="mdi mdi-plus-thick",
                    color=ButtonColorChoices.GREEN,
                    permissions=["nautobot_device_lifecycle_mgmt.add_softwareimagelcm"],
                ),
                PluginMenuButton(
                    link="plugins:nautobot_device_lifecycle_mgmt:softwareimagelcm_import",
                    title="Import",
                    icon_class="mdi mdi-database-import-outline",
                    color=ButtonColorChoices.BLUE,
                    permissions=["nautobot_device_lifecycle_mgmt.add_softwareimagelcm"],
                ),
            ),
        ),
        PluginMenuItem(
            link="plugins:nautobot_device_lifecycle_mgmt:validatedsoftwarelcm_list",
            link_text="Validated Software",
            buttons=(
                PluginMenuButton(
                    link="plugins:nautobot_device_lifecycle_mgmt:validatedsoftwarelcm_add",
                    title="Add",
                    icon_class="mdi mdi-plus-thick",
                    color=ButtonColorChoices.GREEN,
                    permissions=["nautobot_device_lifecycle_mgmt.add_validatedsoftwarelcm"],
                ),
                PluginMenuButton(
                    link="plugins:nautobot_device_lifecycle_mgmt:validatedsoftwarelcm_import",
                    title="Import",
                    icon_class="mdi mdi-database-import-outline",
                    color=ButtonColorChoices.BLUE,
                    permissions=["nautobot_device_lifecycle_mgmt.add_validatedsoftwarelcm"],
                ),
            ),
        ),
        PluginMenuItem(
            link="plugins:nautobot_device_lifecycle_mgmt:cvelcm_list",
            link_text="CVE",
            buttons=(
                PluginMenuButton(
                    link="plugins:nautobot_device_lifecycle_mgmt:cvelcm_add",
                    title="Add",
                    icon_class="mdi mdi-plus-thick",
                    color=ButtonColorChoices.GREEN,
                    permissions=["nautobot_device_lifecycle_mgmt.add_cvelcm"],
                ),
                PluginMenuButton(
                    link="plugins:nautobot_device_lifecycle_mgmt:cvelcm_import",
                    title="Import",
                    icon_class="mdi mdi-database-import-outline",
                    color=ButtonColorChoices.BLUE,
                    permissions=["nautobot_device_lifecycle_mgmt.add_cvelcm"],
                ),
            ),
        ),
        PluginMenuItem(
            link="plugins:nautobot_device_lifecycle_mgmt:vulnerabilitylcm_list",
            link_text="Vulnerability",
        ),
        PluginMenuItem(
            link="plugins:nautobot_device_lifecycle_mgmt:validatedsoftware_device_report",
            link_text="Report: Device OS Validation",
        ),
        PluginMenuItem(
            link="plugins:nautobot_device_lifecycle_mgmt:validatedsoftware_inventoryitem_report",
            link_text="Report: Inventory Item OS Validation",
        ),
    )
