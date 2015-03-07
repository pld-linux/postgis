%define pg_version	%(rpm -q --queryformat '%{VERSION}' postgresql-backend-devel)
%define	beta %{nil}
#
# Conditional build:
%bcond_without  raster	# disable raster support
%bcond_without	doc	# HTML documentation
%bcond_without	gui	# data import GUI
#
Summary:	Geographic Information Systems Extensions to PostgreSQL
Summary(pl.UTF-8):	Rozszerzenie do PostgreSQL wspomagające Geograficzne Systemy Informacyjne
Name:		postgis
Version:	2.1.4
Release:	2
License:	GPL v2+
Group:		Applications/Databases
Source0:	http://download.osgeo.org/postgis/source/%{name}-%{version}%{beta}.tar.gz
# Source0-md5:	6f7bacc0205859dafdfe545db1b892ca
URL:		http://postgis.refractions.net/
%{?with_raster:BuildRequires:	gdal-devel >= 1.6.0}
BuildRequires:	gdal-devel
BuildRequires:	geos-devel >= 3.3.2
BuildRequires:	json-c-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libxml2-devel
BuildRequires:	perl-base
BuildRequires:	postgresql-backend-devel >= 8.3
BuildRequires:	postgresql-devel >= 8.3
BuildRequires:	proj-devel >= 4.5.0
%if %{with doc}
BuildRequires:	ImageMagick
BuildRequires:	docbook-style-xsl
BuildRequires:	libxml2-progs
BuildRequires:	libxslt-progs
%endif
%if %{with gui}
BuildRequires:	gtk+2-devel >= 2:2.8.0
BuildRequires:	pkgconfig
%endif
%{?with_raster:Requires:	gdal >= 1.6.0}
Requires:	liblwgeom = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags_x86_64	-fPIC

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
Requires:	geos >= 3.3.2
Requires:	proj >= 4.5.0
Conflicts:	postgis < 2.0.0-2

%description -n liblwgeom
lwgeom library (a part of PostGIS project).

%description -n liblwgeom -l pl.UTF-8
Biblioteka lwgeom (część projektu PostGIS).

%package -n liblwgeom-devel
Summary:	Header file for lwgeom library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki lwgeom
Group:		Development/Libraries
Requires:	geos-devel >= 3.3.2
Requires:	liblwgeom = %{version}-%{release}
Requires:	proj-devel >= 4.5.0

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
%setup -q -n %{name}-%{version}%{beta}

%build
%configure \
	--with-geos \
	--with-geos-libdir=/usr/%{_lib} \
	%{?with_gui:--with-gui} \
	--with-pgsql \
	--with-proj=%{_prefix} \
	--with-proj-libdir=/usr/%{_lib} \
	%{!?with_raster:--without-raster}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n liblwgeom -p /sbin/ldconfig
%postun	-n liblwgeom -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CREDITS LICENSE.TXT NEWS README.postgis TODO %{?with_doc:doc/html}
%attr(755,root,root) %{_bindir}/pgsql2shp
%attr(755,root,root) %{_bindir}/shp2pgsql
%attr(755,root,root) %{_libdir}/postgresql/postgis-2.1.so
%{_datadir}/postgresql/contrib/postgis-2.1
%if %{with raster}
%attr(755,root,root) %{_bindir}/raster2pgsql
%attr(755,root,root) %{_libdir}/postgresql/rtpostgis-2.1.so
%{_datadir}/postgresql/extension/postgis*.control
%{_datadir}/postgresql/extension/postgis*.sql
%endif

%if %{with gui}
%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/shp2pgsql-gui
%endif

%files -n liblwgeom
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblwgeom-?.?.?.so

%files -n liblwgeom-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblwgeom.so
%{_libdir}/liblwgeom.la
%{_includedir}/liblwgeom.h

%files -n liblwgeom-static
%defattr(644,root,root,755)
%{_libdir}/liblwgeom.a
