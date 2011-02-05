#
%define	snap	20080608 
Summary:	A distributed document-oriented database
Summary(pl.UTF-8):	Rozproszona baza danych oparta o dokumenty
Name:		couchdb
Version:	0.8
Release:	0.%{snap}
License:	Apache
Group:		Applications
Source0:	%{name}-%{version}-%{snap}.tar.gz
# Source0-md5:	f2f7c819f3b562887ed0c336d36c6b38
Source1:	%{name}.init
URL:		http://incubator.apache.org/couchdb/
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	erlang >= 
BuildRequires:	help2man
BuildRequires:	intltool
Requires(post,preun):	/sbin/chkconfig
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Provides:	group(couchdb)
Provides:	user(couchdb)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Apache CouchDB is a distributed, fault-tolerant and schema-free
document-oriented database accessible via a RESTful HTTP/JSON
API. Among other features, it provides robust, incremental replication
with bi-directional conflict detection and resolution, and is
queryable and indexable using a table-oriented view engine with
JavaScript acting as the default view definition language.

%description -l pl.UTF-8

Apache CouchDB jest rozproszoną, odporną na błędy, nie wymagającą
schematów, zorientowaną na dokument bazą danych z RESTowym API opartym
o HTTP/JSON.  Między innymi zapewnia solidną, przyrostową replikację
z dwukierunkowym wykrywaniem i rozwiązywaniem konfliktów, oraz odpytywanie
i indeksowanie za pośrednictwem opartego na tablicach silnika widoków
używającego JavaScriptu jako głównego języka definicji widoku.

%prep
%setup -q -n %{name}
touch ChangeLog # needed by ./configure

%build
./bootstrap
%configure --with-erlang=%{_libdir}/erlang/usr/include
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_defaultdocdir}/*

mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 230 couchdb
%useradd -u 230 -g couchdb -c "CouchDB server" couchdb

%post
/sbin/chkconfig --add %{name}
%service %{name} restart "CouchDB server"

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS CHANGES NEWS NOTICE README THANKS
%attr(755,root,root) %{_bindir}/*
%{_datadir}/apache-couchdb
%{_libdir}/apache-couchdb
%dir %{_sysconfdir}/apache-couchdb/
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache-couchdb/couch.ini
%attr(700,couchdb,couchdb) %dir %{_sharedstatedir}/apache-couchdb
%attr(700,couchdb,couchdb) %dir %{_localstatedir}/log/apache-couchdb
%{_mandir}/man1/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
