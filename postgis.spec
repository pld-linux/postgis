%define pg_version	%(rpm -q --queryformat '%{VERSION}' postgresql-backend-devel)
%define	beta rc2

# Conditional build:
%bcond_without  raster # disable raster support

Summary:	Geographic Information Systems Extensions to PostgreSQL
Summary(pl.UTF-8):	Rozszerzenie do PostgreSQL wspomagające Geograficzne Systemy Informacyjne
Name:		postgis
Version:	2.0.0
Release:	0.%{beta}.1
License:	GPL v2
Group:		Applications/Databases
Source0:	http://postgis.refractions.net/download/%{name}-%{version}%{beta}.tar.gz
# Source0-md5:	2337db7420746aeaeb631c950bbaeb82
URL:		http://postgis.refractions.net/
%{?with_raster:BuildRequires:	gdal-devel >= 1.6.0}
BuildRequires:	geos-devel >= 3.2.0
BuildRequires:	libxml2-devel
BuildRequires:	perl-base
BuildRequires:	postgresql-backend-devel >= 7.1
BuildRequires:	postgresql-devel >= 7.1
BuildRequires:	proj-devel
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

%prep
%setup  -q	-n %{name}-%{version}%{beta}

%build
%configure \
	--with-geos \
	--with-geos-libdir=/usr/%{_lib} \
	--with-pgsql \
	--with-proj=%{_prefix} \
	--with-proj-libdir=/usr/%{_lib} \
	%{!?with_raster:--without-raster}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

# put into lib subpackage if we are interested in the files below?
rm $RPM_BUILD_ROOT%{_includedir}/liblwgeom.h \
	$RPM_BUILD_ROOT%{_libdir}/liblwgeom.a \
	$RPM_BUILD_ROOT%{_libdir}/liblwgeom.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CREDITS NEWS README.postgis TODO doc/html
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/postgresql/*.so*
%{_libdir}/lib*.so
%{_datadir}/postgresql/contrib/postgis-2.0
