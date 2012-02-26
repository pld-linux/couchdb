#
# TODO:
# - init script, sysconfig
# - merge apache-couchdb/apache-couchdb.spec here
#
Summary:	A distributed document-oriented database
Summary(pl.UTF-8):	Rozproszona baza danych oparta o dokumenty
Name:		couchdb
Version:	1.0.1
Release:	0.1
License:	Apache
Group:		Applications
Source0:	http://www.apache.net.pl/couchdb/1.0.1/apache-%{name}-%{version}.tar.gz
# Source0-md5:	001cf286b72492617e9ffba271702a00
#Source1:	%{name}.init
URL:		http://incubator.apache.org/couchdb/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	curl-devel >= 7.18.0
BuildRequires:	erlang
BuildRequires:	help2man
BuildRequires:	intltool
BuildRequires:	js-devel
BuildRequires:	libicu-devel >= 3.4.1
BuildRequires:	pakchois-devel
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
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
%setup -q -n apache-%{name}-%{version}

%build
%configure --with-erlang=%{_libdir}/erlang/usr/include
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_defaultdocdir}/*

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

mv $RPM_BUILD_ROOT/etc/rc.d/{,init.d}/%{name}
#install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

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
%{_datadir}/couchdb
%{_libdir}/couchdb
%dir %{_sysconfdir}/couchdb
%dir %{_sysconfdir}/couchdb/default.d
%dir %{_sysconfdir}/couchdb/local.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/couchdb/*.ini
%attr(700,couchdb,couchdb) %dir %{_sharedstatedir}/couchdb
%attr(700,couchdb,couchdb) %dir %{_localstatedir}/log/couchdb
%{_mandir}/man1/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
#config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
