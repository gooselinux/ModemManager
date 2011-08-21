%define snapshot .git20100628
%define ppp_version 2.4.5
%define realversion 0.4

Summary: Mobile broadband modem management service
Name: ModemManager
Version: 0.4.0
Release: 3%{snapshot}%{?dist}
#
# Source from git://anongit.freedesktop.org/ModemManager/ModemManager
# tarball built with:
#    ./autogen.sh --prefix=/usr --sysconfdir=/etc --localstatedir=/var
#    make distcheck
#
Source: %{name}-%{realversion}%{snapshot}.tar.bz2
License: GPLv2+
Group: System Environment/Base

URL: http://www.gnome.org/projects/NetworkManager/
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires: dbus-glib >= 0.82
Requires: glib2 >= 2.18
BuildRequires: glib2-devel >= 2.18
BuildRequires: dbus-glib-devel >= 0.82
BuildRequires: libgudev-devel >= 143
BuildRequires: ppp = %{ppp_version}
BuildRequires: ppp-devel = %{ppp_version}
BuildRequires: polkit-devel
BuildRequires: automake autoconf intltool libtool
# for xsltproc
BuildRequires: libxslt

Patch0: nm-dbus-glib-disable-legacy-property-access.patch

%description
The ModemManager service provides a consistent API to operate many different
modems, including mobile broadband (3G) devices.

%prep
%setup -q -n %{name}-%{realversion}

%patch0 -p1 -b .dbus-glib-no-legacy-props

%build

autoreconf -i

pppddir=`ls -1d %{_libdir}/pppd/2*`
%configure \
	--enable-more-warnings=yes \
	--with-udev-base-dir=/lib/udev \
	--with-tests=yes \
	--with-docs=yes \
	--disable-static \
	--with-pppd-plugin-dir=$pppddir \
	--with-polkit=no \
	--with-dist-version=%{version}-%{release}

make %{?_smp_mflags}

%check
make check

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/pppd/2.*/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/pppd/2.*/*.so

%post
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :

%files
%defattr(0644, root, root, 0755)
%doc COPYING README
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.ModemManager.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.ModemManager.service
%attr(0755,root,root) %{_sbindir}/modem-manager
%dir %{_libdir}/%{name}
%attr(0755,root,root) %{_libdir}/%{name}/*.so*
/lib/udev/rules.d/*
%{_datadir}/polkit-1/actions/*.policy
%{_datadir}/icons/hicolor/22x22/apps/modem-manager.png

%changelog
* Thu Jul  1 2010 Dan Williams <dcbw@redhat.com> - 0.4.0-3.git20100628
- rpm: bump version to fix RPM version conflicts

* Mon Jun 28 2010 Dan Williams <dcbw@redhat.com> - 0.4-2.git20100628
- core: fix crash during probing when a plugin doesn't support all ports (rh #603294)
- gsm: better registration state checking when devices don't support AT+CREG (Blackberries)
- gsm: add support for getting remaining unlock retry counts

* Tue Jun 22 2010 Dan Williams <dcbw@redhat.com> - 0.4-1.git20100622
- core: fix occasional crash when device is unplugged (rh #591728)
- core: ensure errors are correctly returned when device is unplugged
- core: ensure claimed ports don't fall back to Generic (rh #597296)
- gsm: better compatibility with various phones
- mbm: better detection of connection errors
- simtech: add plugin for Simtech devices (like Airlink 3GU)
- sierra: fix CDMA roaming detection

* Mon May 24 2010 Dan Williams <dcbw@redhat.com> - 0.4.0-0.1
- core: rebuild to fix D-Bus property access (for dbus-glib CVE-2010-1172)
- mbm: catch E2NAP error codes
- simtech: plugin for Simtech-based modems (ie Airlink 3GU)
- sierra: fix CDMA roaming detection

* Fri May  7 2010 Dan Williams <dcbw@redhat.com> - 0.3-13.git20100507
- core: fix crash when plugging in some Sierra and Option NV devices (rh #589798)
- gsm: better compatibility with various Sony Ericsson phones
- longcheer: better support for Alcatel X060s modems

* Tue May  4 2010 Dan Williams <dcbw@redhat.com> - 0.3-12.git20100504
- core: fix data port assignments (rh #587400)

* Sun May  2 2010 Dan Williams <dcbw@redhat.com> - 0.3-11.git20100502
- core: ignore some failures on disconnect (rh #578280)
- core: add support for platform serial devices
- gsm: better Blackberry DUN support
- gsm: periodically poll access technology
- cdma: prevent crash on modem removal (rh #571921)
- mbm: add support for Sony Ericsson MD400, Dell 5541, and Dell 5542 modems
- novatel: better signal strength reporting on CDMA cards
- novatel: add access technology and mode preference support on GSM cards
- zte: fix mode preference retrieval
- longcheer: add support for Zoom modems (4595, 4596, etc)
- longcheer: add access technology and mode preference support

* Fri Apr 30 2010 Matthias Clasen <mclasen@redhat.com> - 0.3-10.git20100409
- Silence %%post
- Update scripts

* Fri Apr  9 2010 Dan Williams <dcbw@redhat.com> - 0.3-9.git20100409
- gsm: fix parsing Blackberry supported character sets response

* Thu Apr  8 2010 Dan Williams <dcbw@redhat.com> - 0.3-8.git20100408
- mbm: fix retrieval of current allowed mode
- gsm: fix initialization issues with some devices (like Blackberries)

* Mon Apr  5 2010 Dan Williams <dcbw@redhat.com> - 0.3-7.git20100405
- core: fix detection of some generic devices (rh #579247)
- core: fix detection regression of some Huawei devices in 0.3-5
- cdma: periodically poll registration state and signal quality
- cdma: really fix registration detection on various devices (rh #569067)

* Wed Mar 31 2010 Dan Williams <dcbw@redhat.com> - 0.3-6.git20100331
- core: fix PPC/SPARC/etc builds

* Wed Mar 31 2010 Dan Williams <dcbw@redhat.com> - 0.3-5.git20100331
- core: only export a modem when all its ports are handled (rh #540438, rh #569067, rh #552121)
- cdma: handle signal quality requests while connected for more devices
- cdma: handle serving system requests while connected for more devices
- gsm: determine current access technology earlier
- huawei: work around automatic registration issues on some devices

* Tue Mar 23 2010 Dan Williams <dcbw@redhat.com> - 0.3-4.git20100323
- core: ensure enabled modems are disabled when MM stops
- core: better capability detection for Blackberry devices (rh #573510)
- cdma: better checking of registration states (rh #540438, rh #569067, rh #552121)
- gsm: don't block modem when it requires PIN2
- option: fix access technology updates

* Wed Mar 17 2010 Dan Williams <dcbw@redhat.com> - 0.3-3.git20100317
- mbm: add device IDs for C3607w
- mbm: fail earlier during connection failures
- mbm: fix username/password authentication when checked by the network
- hso: implement asynchronous signal quality updates
- option: implement asynchronous signal quality updates
- novatel: correctly handle CDMA signal quality
- core: basic PolicyKit support
- core: fix direct GSM registration information requests
- core: general GSM PIN/PUK unlock fixes
- core: poll GSM registration state internally for quicker status updates
- core: implement GSM 2G/3G preference
- core: implement GSM roaming allowed/disallowed preference
- core: emit signals on access technology changes
- core: better handling of disconnections
- core: fix simple CDMA status requests

* Thu Feb 11 2010 Dan Williams <dcbw@redhat.com> - 0.3-2.git20100211
- core: startup speed improvements
- core: GSM PIN checking improvements
- huawei: fix EVDO-only connections on various devices (rh #553199)
- longcheer: add support for more devices

* Tue Jan 19 2010 Dan Williams <dcbw@redhat.com> - 0.3-1.git20100119
- anydata: new plugin for AnyData CDMA modems (rh #547294)
- core: fix crashes when devices are unplugged during operation (rh #553953)
- cdma: prefer primary port for status/registration queries
- core: fix probing/detection of some PIN-locked devices (rh #551376)
- longcheer: add plugin for Alcatel (X020, X030, etc) and other devices
- gsm: fix Nokia N80 network scan parsing

* Fri Jan  1 2010 Dan Williams <dcbw@redhat.com> - 0.2.997-5.git20100101
- core: fix apparent hangs by limiting retried serial writes
- gsm: ensure modem state is reset when disabled

* Fri Dec 18 2009 Dan Williams <dcbw@redhat.com> - 0.2.997-4.git20091218
- sierra: fix CDMA registration detection in some cases (rh #547513)

* Wed Dec 16 2009 Dan Williams <dcbw@redhat.com> - 0.2.997-3.git20091216
- sierra: ensure CDMA device is powered up when trying to use it
- cdma: better signal quality parsing (fixes ex Huawei EC168C)
- zte: handle unsolicited messages better during probing

* Mon Dec 14 2009 Dan Williams <dcbw@redhat.com> - 0.2.997-2.git20091214
- cdma: fix signal strength reporting on some devices
- cdma: better registration state detection when dialing (ex Sierra 5275)
- option: always use the correct tty for dialing commands

* Mon Dec  7 2009 Dan Williams <dcbw@redhat.com> - 0.2.997-1
- core: fix reconnect after manual disconnect (rh #541314)
- core: fix various segfaults during registration
- core: fix probing of various modems on big-endian architectures (ie PPC)
- core: implement modem states to avoid duplicate operations
- hso: fix authentication for Icera-based devices like iCON 505
- zte: use correct port for new devices
- nozomi: fix detection

* Thu Nov  5 2009 Dan Williams <dcbw@redhat.com> - 0.2-4.20091105
- Update to latest git
- core: fix pppd 2.4.5 errors about 'baudrate 0'
- cdma: wait for network registration before trying to connect
- gsm: add cell access technology reporting
- gsm: allow longer-running network scans
- mbm: various fixes for Ericsson F3507g/F3607gw/Dell 5530
- nokia: don't power down phones on disconnect
- hso: fix disconnection/disable

* Wed Aug 26 2009 Dan Williams <dcbw@redhat.com> - 0.2-3.20090826
- Fixes for Motorola and Ericsson devices
- Fixes for CDMA "serving-system" command parsing

* Fri Jul 31 2009 Matthias Clasen <mclasen@redhat.com>
- Fix a typo in one of the udev rules files

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-2.20090707
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 7 2009 Dan Williams <dcbw@redhat.com> - 0.2-1.20090707
- Fix source repo location
- Fix directory ownership

* Tue Jul 7 2009 Dan Williams <dcbw@redhat.com> - 0.2-0.20090707
- Initial version

