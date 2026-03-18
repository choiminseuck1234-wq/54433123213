import zipfile
import os
import shutil
import tempfile
from xml.etree import ElementTree as ET


def merge_hwpx(files, output_path):
    temp_dir = tempfile.mkdtemp()

    merged_sections = []

    for i, file in enumerate(files):
        extract_dir = os.path.join(temp_dir, f"file_{i}")
        os.makedirs(extract_dir, exist_ok=True)

        with zipfile.ZipFile(file, 'r') as z:
            z.extractall(extract_dir)

        section_path = os.path.join(extract_dir, "Contents", "section0.xml")

        if os.path.exists(section_path):
            tree = ET.parse(section_path)
            root = tree.getroot()
            merged_sections.append(root)

    # 첫 파일 기준
    base_dir = os.path.join(temp_dir, "base")
    with zipfile.ZipFile(files[0], 'r') as z:
        z.extractall(base_dir)

    base_section = os.path.join(base_dir, "Contents", "section0.xml")
    base_tree = ET.parse(base_section)
    base_root = base_tree.getroot()

    for section in merged_sections[1:]:
        for elem in section:
            base_root.append(elem)

    base_tree.write(base_section, encoding="utf-8", xml_declaration=True)

    # 다시 압축
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, base_dir)
                z.write(full_path, rel_path)

    shutil.rmtree(temp_dir)
