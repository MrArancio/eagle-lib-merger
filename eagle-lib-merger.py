import glob
import os
from lxml import etree as et

outfile = 'SeeedFusion.lbr'
os.remove(outfile)

eagle = et.Element('eagle')
eagle.attrib['version'] = '6.4'
drawing = et.SubElement(eagle, 'drawing')

librerie = glob.glob('*.lbr')

packagesNode = None
symbolsNode = None
devicesetsNode = None
settings = None
grid = None
layers = None

packageNames = {}
symbolNames = {}
devicesetsNames = {}



first = True
for lib in librerie:
    print "Opening library '" + lib + "'..."
    f = open(lib)
    tree = et.parse(f)
    if first:
        settings = tree.xpath('/eagle/drawing/settings')[0]
        grid = tree.xpath('/eagle/drawing/grid')[0]
        layers = tree.xpath('/eagle/drawing/layers')[0]
        drawing.append(settings)
        drawing.append(grid)
        drawing.append(layers)
        library = et.SubElement(drawing, 'library')
        packagesNode = et.SubElement(library, 'packages')
        symbolsNode = et.SubElement(library, 'symbols')
        devicesetsNode = et.SubElement(library, 'devicesets')
        first = False

    packages = tree.xpath('/eagle/drawing/library/packages/package')
    for package in packages:
        name = package.attrib['name']
        if name not in packageNames:
            print "Package '"+name+"' added."
            packageNames[name] = {}
            packageNames[name][lib] = name
        else:
            n_doppioni = len(packageNames[name])
            new_name = name + "#" + str(n_doppioni)
            packageNames[name][lib] = new_name
            package.attrib['name'] = new_name
            print "Package '" + name + "' already present, renamed to '" + new_name + "'."
        packagesNode.append(package)

    symbols = tree.xpath('/eagle/drawing/library/symbols/symbol')
    for symbol in symbols:
        name = symbol.attrib['name']
        if name not in symbolNames:
            print "Symbol '"+name+"' added."
            symbolNames[name] = {}
            symbolNames[name][lib] = name
        else:
            n_doppioni = len(symbolNames[name])
            new_name = name + "#" + str(n_doppioni)
            symbolNames[name][lib] = new_name
            symbol.attrib['name'] = new_name
            print "Symbol '" + name + "' already present, renamed to '" + new_name + "'."
        symbolsNode.append(symbol)

    devicesets = tree.xpath('/eagle/drawing/library/devicesets/deviceset')
    for deviceset in devicesets:
        name = deviceset.attrib['name']
        if name not in devicesetsNames:
            print "Deviceset '"+name+"' added."
            devicesetsNames[name] = {}
            devicesetsNames[name][lib] = name
        else:
            n_doppioni = len(devicesetsNames[name])
            new_name = name + "#" + str(n_doppioni)
            devicesetsNames[name][lib] = new_name
            deviceset.attrib['name'] = new_name
            print "Deviceset '" + name + "' already present, renamed to '" + new_name + "'."

        # 1. rename symbol in gates
        gates = deviceset.xpath('gates/gate')
        for gate in gates:
            symbolName = gate.attrib['symbol']
            new_name = symbolNames[symbolName][lib]
            gate.attrib['symbol'] = new_name
        # 2. rename package in device
        devices = deviceset.xpath('devices/device')
        for device in devices:
            if 'package' in device.attrib:
                deviceName = device.attrib['package']
                new_name = packageNames[deviceName][lib]
                device.attrib['package'] = new_name

        devicesetsNode.append(deviceset)


tree = et.ElementTree(eagle)
tree.write(outfile, pretty_print=True, xml_declaration=True, encoding="utf-8")
