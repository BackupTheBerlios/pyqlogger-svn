# $Id: pyqlogger-1.3.2.ebuild 29 2004-12-06 10:50:52Z mightor $

inherit eutils distutils

MY_P=PyQLogger-${PV/_/}
S=${WORKDIR}/${MY_P}

DESCRIPTION="PyQT Blogger Client"
SRC_URI="http://download.berlios.de/pyqlogger/${MY_P}.tar.gz"
HOMEPAGE="http://pyqlogger.berlios.de/"

SLOT="0"
LICENSE="GPL-2"
KEYWORDS="x86 ~ppc"

DEPEND="virtual/python
	dev-python/pyosd
	>=dev-python/PyQt-3.12"

src_compile() {
	cd ${S}
	distutils_python_version
}

src_install() {
	python setup.py --install || die
}
