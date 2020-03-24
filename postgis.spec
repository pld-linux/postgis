# TODO: sfcgal support (sfcgal-config, >= 1.1.0)
%define pg_version	%(rpm -q --queryformat '%{VERSION}' postgresql-backend-devel)
#
# Conditional build:
%bcond_without  raster	# disable raster support
%bcond_without	doc	# HTML documentation
%bcond_without	gui	# data import GUI
#
Summary:	Geographic Information Systems Extensions to PostgreSQL
Summary(pl.UTF-8):	Rozszerzenie do PostgreSQL wspomagające Geograficzne Systemy Informacyjne
Name:		postgis
Version:	3.0.0
%define	subver %{nil}
Release:	5
License:	GPL v2+
Group:		Applications/Databases
Source0:	https://download.osgeo.org/postgis/source/%{name}-%{version}%{subver}.tar.gz
# Source0-md5:	725019e3a67ac52ccef4d00031cb0c77
Patch0:		install-lwgeom.patch
URL:		http://postgis.refractions.net/
%{?with_raster:BuildRequires:	gdal-devel >= 1.8.0}
BuildRequires:	clang
BuildRequires:	geos-devel >= 3.5.0
BuildRequires:	json-c-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	pcre-devel
BuildRequires:	perl-base
BuildRequires:	postgresql-backend-devel >= 9.1
BuildRequires:	postgresql-devel >= 9.1
BuildRequires:	proj-devel >= 4.6.0
%if %{with doc}
BuildRequires:	ImageMagick
BuildRequires:	docbook-style-xsl
BuildRequires:	libxml2-progs
BuildRequires:	libxslt-progs
# TODO: mathml DTD (http://www.w3.org/Math/DTD/mathml2/mathml2.dtd, e.g. /usr/share/xml/schema/w3c/mathml/dtd)
%endif
%if %{with gui}
BuildRequires:	gtk+2-devel >= 2:2.8.0
BuildRequires:	pkgconfig
%endif
%{?with_raster:Requires:	gdal >= 1.8.0}
Requires:	liblwgeom = %{version}-%{release}
Requires:	postgresql >= %{pg_version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags_x86_64	-fPIC

# clang can't parse this
%define		filterout		-fvar-tracking-assignments

# oh well... I also don't understand this... ;)

%description
This package contains a module which implements GIS simple features,
ties the features to rtree indexing, and provides some spatial
functions for accessing and analyzing geographic data.

%description -l pl.UTF-8
Pakiet ten zawiera moduł implementujący proste funkcje GIS, wiąże je z
indeksowaniem rtree oraz dostarcza funkcje dostępu oraz analizy danych
geograficznych.

%package gui
Summary:	Data import GUI for PostGIS
Summary(pl.UTF-8):	Graficzny interfejs użytkownika importujący dane dla PostGIS-a
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	gtk+2 >= 2:2.8.0

%description gui
Data import GUI for PostGIS.

%description gui -l pl.UTF-8
Graficzny interfejs użytkownika importujący dane dla PostGIS-a.

%package -n liblwgeom
Summary:	lwgeom library (a part of PostGIS project)
Summary(pl.UTF-8):	Biblioteka lwgeom (część projektu PostGIS)
Group:		Libraries
Requires:	geos >= 3.5.0
Requires:	proj >= 4.6.0
Conflicts:	postgis < 2.0.0-2

%description -n liblwgeom
lwgeom library (a part of PostGIS project).

%description -n liblwgeom -l pl.UTF-8
Biblioteka lwgeom (część projektu PostGIS).

%package -n liblwgeom-devel
Summary:	Header file for lwgeom library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki lwgeom
Group:		Development/Libraries
Requires:	geos-devel >= 3.5.0
Requires:	liblwgeom = %{version}-%{release}
Requires:	proj-devel >= 4.6.0

%description -n liblwgeom-devel
Header file for lwgeom library.

%description -n liblwgeom-devel -l pl.UTF-8
Plik nagłówkowy biblioteki lwgeom.

%package -n liblwgeom-static
Summary:	Static lwgeom library
Summary(pl.UTF-8):	Statyczna biblioteka lwgeom
Group:		Development/Libraries
Requires:	liblwgeom-devel = %{version}-%{release}

%description -n liblwgeom-static
Static lwgeom library.

%description -n liblwgeom-static -l pl.UTF-8
Statyczna biblioteka lwgeom.

%prep
%setup -q -n %{name}-%{version}%{subver}
%patch0 -p1

%build
export CFLAGS="%{rpmcflags} -DACCEPT_USE_OF_DEPRECATED_PROJ_API_H"
%configure \
	%{?with_gui:--with-gui} \
	%{!?with_raster:--without-raster}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__sed} -e '/#include .*/d' postgis_config.h > $RPM_BUILD_ROOT%{_includedir}/postgis_config.h
%{__sed} -i -e 's/#include.*postgis_config.*/#include "postgis_config.h"/' $RPM_BUILD_ROOT%{_includedir}/liblwgeom.h

# Fix icons and desktop file locations
%{__mv} $RPM_BUILD_ROOT%{_datadir}/{postgresql,}/icons
%{__mv} $RPM_BUILD_ROOT%{_datadir}/{postgresql,}/applications

%{__rm} -r $RPM_BUILD_ROOT%{_iconsdir}/hicolor/40x40

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n liblwgeom -p /sbin/ldconfig
%postun	-n liblwgeom -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CREDITS LICENSE.TXT NEWS README.postgis TODO %{?with_doc:doc/html}
%attr(755,root,root) %{_bindir}/pgsql2shp
%attr(755,root,root) %{_bindir}/shp2pgsql
%attr(755,root,root) %{_libdir}/postgresql/postgis-3.so
%attr(755,root,root) %{_libdir}/postgresql/postgis_raster-3.so
%attr(755,root,root) %{_libdir}/postgresql/postgis_topology-3.so
%{_datadir}/postgresql/contrib/postgis-3.0
%if %{with raster}
%attr(755,root,root) %{_bindir}/raster2pgsql
%{_datadir}/postgresql/extension/postgis*.control
%{_datadir}/postgresql/extension/postgis*.sql
%endif
%{_libdir}/postgresql/address_standardizer-3.so
%{_datadir}/postgresql/extension/address_standardizer*.sql
%{_datadir}/postgresql/extension/address_standardizer*.control
%dir %{_libdir}/postgresql/bitcode
%{_libdir}/postgresql/bitcode/address_standardizer-3.index.bc
%dir %{_libdir}/postgresql/bitcode/address_standardizer-3/
%{_libdir}/postgresql/bitcode/address_standardizer-3/*.bc
%{_libdir}/postgresql/bitcode/postgis-3.index.bc
%dir %{_libdir}/postgresql/bitcode/postgis-3
%{_libdir}/postgresql/bitcode/postgis-3/*.bc
%{_libdir}/postgresql/bitcode/postgis_raster-3.index.bc
%dir %{_libdir}/postgresql/bitcode/postgis_raster-3
%{_libdir}/postgresql/bitcode/postgis_raster-3/*.bc
%{_libdir}/postgresql/bitcode/postgis_topology-3.index.bc
%dir %{_libdir}/postgresql/bitcode/postgis_topology-3
%{_libdir}/postgresql/bitcode/postgis_topology-3/*.bc

%if %{with gui}
%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/shp2pgsql-gui
%{_desktopdir}/shp2pgsql-gui.desktop
%{_iconsdir}/hicolor/*x*/apps/shp2pgsql-gui.png
%endif

%files -n liblwgeom
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblwgeom-3.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblwgeom-3.0.so.0

%files -n liblwgeom-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblwgeom.so
%{_libdir}/liblwgeom.la
%{_includedir}/liblwgeom.h
%{_includedir}/liblwgeom_topo.h
%{_includedir}/lwinline.h
%{_includedir}/postgis_config.h

%files -n liblwgeom-static
%defattr(644,root,root,755)
%{_libdir}/liblwgeom.a
