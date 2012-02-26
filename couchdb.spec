#
# TODO:
# - init script, sysconfig
# - merge apache-couchdb/apache-couchdb.spec here
# - tmpfiles.d
# - system packages:
#   erlang-ibrowse >= 2.2.0
#   erlang-mochiweb
#   erlang-oauth

%define		mochiwebver	r113
%define		ibrowsever	2.2.0
%define		erlangver	 1:R12B5
Summary:	A document database server, accessible via a RESTful JSON API
Summary(pl.UTF-8):	Rozproszona baza danych oparta o dokumenty
Name:		couchdb
Version:	1.0.3
Release:	0.1
License:	Apache v2.0
Group:		Applications/Databases
Source0:	http://www.apache.org/dist/couchdb/%{version}/apache-%{name}-%{version}.tar.gz
# Source0-md5:	cfdc2ab751bf18049c5ef7866602d8ed
Source1:	%{name}.init
Source2:	%{name}.tmpfiles
URL:		http://couchdb.apache.org/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1.6.3
BuildRequires:	curl-devel >= 7.18.0
BuildRequires:	erlang >= %{erlangver}
BuildRequires:	help2man
BuildRequires:	intltool
BuildRequires:	js-devel >= 1.8
BuildRequires:	libicu-devel >= 3.4.1
BuildRequires:	libtool
BuildRequires:	pakchois-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.647
Requires(post,preun):	/sbin/chkconfig
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	erlang >= %{erlangver}
Provides:	group(couchdb)
Provides:	user(couchdb)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Apache CouchDB is a distributed, fault-tolerant and schema-free
document-oriented database accessible via a RESTful HTTP/JSON API.
Among other features, it provides robust, incremental replication with
bi-directional conflict detection and resolution, and is queryable and
indexable using a table-oriented view engine with JavaScript acting as
the default view definition language.

%description -l pl.UTF-8
Apache CouchDB jest rozproszoną, odporną na błędy, nie wymagającą
schematów, zorientowaną na dokument bazą danych z RESTowym API opartym
o HTTP/JSON. Między innymi zapewnia solidną, przyrostową replikację z
dwukierunkowym wykrywaniem i rozwiązywaniem konfliktów, oraz
odpytywanie i indeksowanie za pośrednictwem opartego na tablicach
silnika widoków używającego JavaScriptu jako głównego języka definicji
widoku.

%prep
%setup -q -n apache-%{name}-%{version}

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-erlang=%{_libdir}/erlang%{_includedir} \

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}
mv $RPM_BUILD_ROOT%{_sysconfdir}/default/couchdb $RPM_BUILD_ROOT/etc/sysconfig

%{__rm} $RPM_BUILD_ROOT/etc/rc.d/%{name}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

install -d $RPM_BUILD_ROOT%{systemdtmpfilesdir}
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 203 -r -f couchdb
%useradd -u 203 -r -d /var/lib/couchdb -s /bin/sh -c "CouchDB Administrator" -g couchdb couchdb

%post
/sbin/chkconfig --add %{name}
%service %{name} restart "CouchDB server"

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" = "0" ]; then
	%userremove couchdb
	%groupremove couchdb
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS CHANGES NEWS NOTICE README THANKS
%dir %{_sysconfdir}/couchdb
%dir %{_sysconfdir}/couchdb/default.d
%attr(755,couchdb,couchdb) %dir %{_sysconfdir}/couchdb/local.d
%attr(644,couchdb,couchdb) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/couchdb/default.ini
%attr(644,couchdb,couchdb) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/couchdb/local.ini

%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%{systemdtmpfilesdir}/couchdb.conf

# XXX: sbindir?
%attr(755,root,root) %{_bindir}/couchdb
%attr(755,root,root) %{_bindir}/couchjs
%{_mandir}/man1/couchdb.1*
%{_mandir}/man1/couchjs.1*

%dir %{_libdir}/couchdb

%dir %{_libdir}/couchdb/bin
%attr(755,root,root) %{_libdir}/couchdb/bin/couchjs

%dir %{_libdir}/couchdb/erlang
%dir %{_libdir}/couchdb/erlang/lib
# XXX: better have unversioned dirs?
%dir %{_libdir}/couchdb/erlang/lib/couch-%{version}
%dir %{_libdir}/couchdb/erlang/lib/couch-%{version}/ebin
%{_libdir}/couchdb/erlang/lib/couch-%{version}/ebin/*.beam
%{_libdir}/couchdb/erlang/lib/couch-%{version}/ebin/*.app
# XXX check if this include is needed runtime
%dir %{_libdir}/couchdb/erlang/lib/couch-%{version}/include
%{_libdir}/couchdb/erlang/lib/couch-%{version}/include/couch_db.hrl
%{_libdir}/couchdb/erlang/lib/couch-%{version}/include/couch_js_functions.hrl

%dir %{_libdir}/couchdb/erlang/lib/couch-%{version}/priv
%{_libdir}/couchdb/erlang/lib/couch-%{version}/priv/couchspawnkillable
%{_libdir}/couchdb/erlang/lib/couch-%{version}/priv/stat_descriptions.cfg

%dir %{_libdir}/couchdb/erlang/lib/couch-%{version}/priv/lib
# XXX: check if .la is needed
%{_libdir}/couchdb/erlang/lib/couch-%{version}/priv/lib/couch_icu_driver.la
%attr(755,root,root) %{_libdir}/couchdb/erlang/lib/couch-%{version}/priv/lib/couch_icu_driver.so

# XXX: better have unversioned dirs?
%dir %{_libdir}/couchdb/erlang/lib/mochiweb-%{mochiwebver}
%dir %{_libdir}/couchdb/erlang/lib/mochiweb-%{mochiwebver}/ebin
%{_libdir}/couchdb/erlang/lib/mochiweb-%{mochiwebver}/ebin/*.beam
%{_libdir}/couchdb/erlang/lib/mochiweb-%{mochiwebver}/ebin/*.app

%dir %{_libdir}/couchdb/erlang/lib/etap
%{_libdir}/couchdb/erlang/lib/etap/ebin

%dir %{_libdir}/couchdb/erlang/lib/erlang-oauth
%{_libdir}/couchdb/erlang/lib/erlang-oauth/ebin

%dir %{_libdir}/couchdb/erlang/lib/ibrowse-%{ibrowsever}
%{_libdir}/couchdb/erlang/lib/ibrowse-%{ibrowsever}/ebin

%{_datadir}/couchdb

%attr(700,couchdb,couchdb) %dir %{_sharedstatedir}/couchdb

%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/couchdb
%attr(700,couchdb,couchdb) %dir %{_localstatedir}/log/couchdb

%attr(755,couchdb,root) %dir /var/run/couchdb
