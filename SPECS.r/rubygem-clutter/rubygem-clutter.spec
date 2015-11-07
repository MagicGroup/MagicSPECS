%global	gem_name	clutter

Name:		rubygem-%{gem_name}
Version:	2.2.5
Release:	4%{?dist}
Summary:	Ruby binding of Clutter

License:	LGPLv2+
URL:		http://ruby-gnome2.sourceforge.jp/
Source0:	https://rubygems.org/gems/%{gem_name}-%{version}.gem
# https://raw.github.com/ruby-gnome2/ruby-gnome2/master/COPYING.LIB
Source1:	COPYING.LIB.clutter

BuildRequires:	ruby(release)
BuildRequires:	rubygems-devel
BuildRequires:	clutter
BuildRequires:	rubygem(cairo-gobject)
BuildRequires:	rubygem-glib2-devel
BuildRequires:	rubygem(gobject-introspection)
BuildRequires:	rubygem(pango)
BuildRequires:	rubygem(test-unit)
BuildRequires:	rubygem(test-unit-notify)
# Need X
BuildRequires:	%{_bindir}/xvfb-run
BuildRequires:	mesa-dri-drivers
Requires:	ruby(release)
Requires:	ruby(rubygems)
Requires:	clutter
Requires:	rubygem(cairo-gobject)
Requires:	rubygem(gobject-introspection)
BuildArch:	noarch
Provides:	rubygem(%{gem_name}) = %{version}-%{release}

%description
Ruby/Clutter is a Ruby binding of Clutter.


%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description	doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

sed -i -e 's|= 2\.2\.5|>= 2.2.5|' %{gem_name}.gemspec

# Add license text
install -cpm 644 %{SOURCE1} ./COPYING.LIB
sed -i -e '/files =/s|\("Rakefile",\)|\1 "COPYING.LIB", |' \
	%{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}

# kill unneeded make process
rm -rf ./TMPBINDIR
mkdir ./TMPBINDIR
pushd ./TMPBINDIR
ln -sf /bin/true make
export PATH=$(pwd):$PATH
popd

# Tweak test source directory
sed -i.path \
	-e '\@^clutter_base =@s|^.*$|clutter_base = File.join(File.dirname(__FILE__), "..")|' \
	test/run-test.rb

mkdir tmp
touch tmp/gobject-introspection-test-utils.rb

# Need X
# For screen depth 24, see bug 904851
# Currently test fails:
# https://github.com/ruby-gnome2/ruby-gnome2/issues/268
xvfb-run \
	-s "-screen 0 640x480x24" \
%if 0
	-e /dev/stderr \
%endif
	ruby -Ilib:tmp:test ./test/run-test.rb

mv test/run-test.rb{.path,}
rm -rf tmp/

popd

%files
%%doc	%{gem_instdir}/[A-Z]*
%exclude	%{gem_instdir}/Rakefile
%dir	%{gem_instdir}/
%dir	%{gem_instdir}/lib/
%{gem_instdir}/lib/%{gem_name}.rb
%dir	%{gem_instdir}/lib/%{gem_name}
%{gem_instdir}/lib/%{gem_name}/*.rb

%exclude %{gem_cache}
%{gem_spec}

%files	doc
%doc	%{gem_docdir}
# Contains really executable sample scripts
%{gem_instdir}/sample/
%exclude	%{gem_instdir}/test/

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 2.2.5-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.2.5-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 29 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.5-1
- 2.2.5

* Sun Dec 28 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.4-1
- 2.2.4

* Sun Nov 23 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.3-2
- Test failure was fixed on gobject-introspection side,
  removing rescue and rebuild

* Thu Nov 20 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.3-1
- 2.2.3

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 14 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.0-1
- 2.2.0

* Sun Jan 19 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.1.0-1
- 2.1.0

* Sun Jan 19 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.0.2-1
- Initial package
