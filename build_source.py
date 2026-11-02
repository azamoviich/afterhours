#!/usr/bin/env python3
"""Regenerates apps.json (AltStore/SideStore source format).
Usage: python3 build_source.py https://azamoviich.github.io/afterhours"""
import json, os, sys, datetime
BASE = (sys.argv[1] if len(sys.argv) > 1 else "https://REPLACE_ME").rstrip("/")
here = os.path.dirname(os.path.abspath(__file__))
today = datetime.date.today().isoformat()
size = lambda f: os.path.getsize(os.path.join(here, "ipa", f))

apps = [
    dict(name="Nudge", bundleIdentifier="uz.plagueson.nudge", developerName="Plagueson",
         subtitle="A demo to-do app for people who forget.",
         localizedDescription="Type tasks like you think (\"call mom tomorrow 6pm #personal !!\"), brain-dump a whole list at once, "
                              "and get nagged until it's done. Morning digest, snooze from the notification, repeating tasks. Just a demo app I made in my free time.",
         iconURL=f"{BASE}/img/nudge-icon.png", tintColor="FF5A36", category="productivity", screenshots=[f"{BASE}/img/nudge-{i}.jpg" for i in (1, 2, 3, 4)],
         versions=[dict(version="1.1", buildVersion="3", date=today,
                        localizedDescription="Widgets! Home screen (small/medium/large, tick tasks right on the widget) and lock screen. Note: the widget uses 1 extra App ID on free accounts.",
                        downloadURL=f"{BASE}/ipa/Nudge.ipa", size=size("Nudge.ipa"), minOSVersion="26.0")],
         appPermissions=dict(entitlements=[], privacy={})),
    dict(name="Blare", bundleIdentifier="uz.plagueson.blare", developerName="Plagueson",
         subtitle="A loud alarm that actually wakes you.",
         localizedDescription="Real system alarms (AlarmKit) that ring through Silent and Focus, with 5 very loud sounds. "
                              "Wake-up missions (math, shake, type) and No Escape mode: hit Stop without finishing and it rings again every minute. "
                              "Just a demo app I made in my free time.",
         iconURL=f"{BASE}/img/blare-icon.png", tintColor="FF3B1F", category="utilities",
         screenshots=[f"{BASE}/img/blare-{i}.jpg" for i in (1, 2, 3, 4)],
         versions=[dict(version="1.0", buildVersion="1", date=today, localizedDescription="First release.",
                        downloadURL=f"{BASE}/ipa/Blare.ipa", size=size("Blare.ipa"), minOSVersion="26.0")],
         appPermissions=dict(entitlements=[], privacy={"NSAlarmKitUsageDescription": "Schedules real alarms that ring on silent.",
                                                      "NSMotionUsageDescription": "Counts shakes for the shake mission."})),
    dict(name="Benefit Motors", bundleIdentifier="uz.benefitmotors.app", developerName="Benefit Motors",
         subtitle="Demo car dealership app.",
         localizedDescription="Browse inventory, calculate financing, book a test drive and get a trade-in estimate. Just a demo app I made in my free time — not a real store, all cars and prices are made up.",
         iconURL=f"{BASE}/img/benefit-icon.png", tintColor="111111", category="lifestyle",
         screenshots=[f"{BASE}/img/benefit-{i}.jpg" for i in (1, 2, 3, 4)],
         versions=[dict(version="1.0", buildVersion="1", date=today, localizedDescription="Demo release.",
                        downloadURL=f"{BASE}/ipa/BenefitMotors.ipa", size=size("BenefitMotors.ipa"), minOSVersion="26.0")],
         appPermissions=dict(entitlements=[], privacy={})),
]
source = dict(name="afterhours", identifier="uz.plagueson.afterhours", subtitle="Apps I build after hours",
              description="Small, polished iOS apps made in my free time.", website="https://azamoviich.github.io/afterhours",
              headerURL=f"{BASE}/img/banner.png",
              iconURL=f"{BASE}/img/nudge-icon.png", tintColor="FF5A36", apps=apps, news=[])
json.dump(source, open(os.path.join(here, "apps.json"), "w"), indent=2, ensure_ascii=False)
print(f"apps.json written for {BASE}")
