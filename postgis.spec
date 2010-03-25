%define pg_version	%(rpm -q --queryformat '%{VERSION}' postgresql-backend-devel)
%define	beta %{nil}
Summary:	Geographic Information Systems Extensions to PostgreSQL
Summary(pl.UTF-8):	Rozszerzenie do PostgreSQL wspomagające Geograficzne Systemy Informacyjne
Name:		postgis
Version:	1.5.1
Release:	1
License:	GPL v2
Group:		Applications/Databases
Source0:	http://postgis.refractions.net/download/%{name}-%{version}%{beta}.tar.gz
# Source0-md5:	8353b38c38282b2192f01693f71b8d28
URL:		http://postgis.refractions.net/
BuildRequires:	geos-devel >= 3.1.1
BuildRequires:	libxml2-devel
BuildRequires:	perl-base
BuildRequires:	postgresql-backend-devel >= 7.1
BuildRequires:	postgresql-devel >= 7.1
BuildRequires:	proj-devel
Requires:	postgresql-module-plpgsql = %{pg_version}
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
	--with-proj-libdir=/usr/%{_lib}

%{__make} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcppflags} %{rpmcflags}" \
	LPATH="%{_libdir}/postgresql" \
	shlib="%{name}.so"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/postgresql,%{_bindir},%{_datadir}/postgresql/contrib}

%{__make} -C loader install \
	bindir="$RPM_BUILD_ROOT%{_bindir}" \
    PGSQL_BINDIR="$RPM_BUILD_ROOT%{_bindir}" \
	INSTALL_PROGRAM=install

sed -i 's#\$libdir/postgis-1.4#%{_libdir}/postgresql/postgis#g' postgis/postgis*.sql
install postgis/*.so* $RPM_BUILD_ROOT%{_libdir}/postgresql
install postgis/*.sql *.sql $RPM_BUILD_ROOT%{_datadir}/postgresql/contrib

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CREDITS NEWS README.postgis TODO doc/html
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/postgresql/*.so*
%{_datadir}/postgresql/contrib/*.sql
