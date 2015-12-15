#! /bin/sh

# Get psi sources
rm -fr psi
git clone --depth 1 git://github.com/psi-im/psi.git
pushd psi
git submodule init
git submodule update
popd

# Get psi-dev repositoris
rm -fr main plugins
git clone git://github.com/psi-plus/main.git
git clone --depth 1 git://github.com/psi-plus/plugins.git

# Prepare
pushd main
rev=$(echo $((`git describe --tags | cut -d - -f 2`)))
pkgrev=$(date +%Y%m%d)git${rev}
psiver=0.16-${pkgrev}
popd

# Translations
rm -fr psi-plus-l10n
git clone --depth 1 git://github.com/psi-plus/psi-plus-l10n.git
pushd psi-plus-l10n
rev_l10n=$(git rev-parse --short HEAD)
echo
tar --exclude='.*' -cjf ../psi-plus-l10n-${rev_l10n}.tar.bz2 translations
popd
rm -fr psi-plus-l10n

# Prepare psi-plus folder
rm -fr psi-plus-${psiver}
mkdir psi-plus-${psiver}
cp -r psi/* psi/.qmake.cache.in psi-plus-${psiver}
rm -fr psi

# Copy plugins sources to psi dir
cp -r plugins/* psi-plus-${psiver}/src/plugins
rm -fr plugins

# Apply patches
cat main/patches/*.diff | patch -s --no-backup-if-mismatch -d psi-plus-${psiver} -p1
cp -r main/iconsets/* psi-plus-${psiver}/iconsets

rm -fr main

# Drop generating files
rm -f psi-plus-${psiver}/configure*

echo "0.16.${rev}-webkit (@@DATE@@)" > psi-plus-${psiver}/version
find psi-plus-${psiver} -name '.*' > exclude.files
sed -i "/psi-plus-${psiver}\/.qmake.cache.in/d" exclude.files
tar -X exclude.files -cjf psi-plus-${psiver}.tar.bz2 psi-plus-${psiver}
rm -fr psi-plus-${psiver} exclude.files exclude.files.backup
