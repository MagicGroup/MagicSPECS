Name:		lzma-sdk457
Version:	4.57
Release:	4%{?dist}
Summary:	SDK for lzma compression
Summary(zh_CN.UTF-8): lzma 压缩的 SDK
Group:		Applications/Archiving
Group(zh_CN.UTF-8): 应用程序/归档
License:	LGPLv2+
URL:		http://sourceforge.net/projects/sevenzip/
Source0:	http://downloads.sourceforge.net/sevenzip/lzma457.tar.bz2
Source1:	http://www.gnu.org/licenses/lgpl-2.1.txt
Patch0:		lzma-sdk-4.5.7-sharedlib.patch
Patch1:		lzma-sdk-4.5.7-format-security-fix.patch

%description
LZMA SDK provides the documentation, samples, header files, libraries,
and tools you need to develop applications that use LZMA compression.

LZMA is default and general compression method of 7z format
in 7-Zip compression program (7-zip.org). LZMA provides high
compression ratio and very fast decompression.

LZMA is an improved version of famous LZ77 compression algorithm. 
It was improved in way of maximum increasing of compression ratio,
keeping high decompression speed and low memory requirements for
decompressing.

%description -l zh_CN.UTF-8
lzma 压缩的 SDK，这是 4.57 版本。

%package devel
Summary:	Development libraries and headers for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Development libraries and headers for %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -c -n lzma457
%patch0 -p1 -b .shared
%patch1 -p1 -b .format-security
# Fix FSF mailing address
rm LGPL.txt
cp %{SOURCE1} LGPL.txt
rm lzma.exe

for f in .h .c .cpp .dsw .dsp .java .cs .txt makefile; do
	find . -iname "*$f" | xargs chmod -x
done

# correct end-of-line encoding
sed -i 's/\r//' *.txt 

for i in \
7zFormat.txt \
CS/7zip/Compress/LzmaAlone/LzmaAlone.sln \
7zC.txt \
CS/7zip/Compress/LzmaAlone/LzmaAlone.csproj \
CPP/7zip/Bundles/Alone7z/resource.rc \
history.txt \
lzma.txt \
CPP/7zip/Compress/LZMA_Alone/makefile.gcc \
CPP/Build.mak \
CPP/7zip/Bundles/Format7zR/resource.rc \
C/Archive/7z/makefile.gcc \
CPP/7zip/Archive/Archive.def \
CPP/7zip/Bundles/Format7zExtractR/resource.rc \
CPP/7zip/Archive/Archive2.def \
CPP/7zip/MyVersionInfo.rc \
Methods.txt; do
	iconv -f iso-8859-1 -t utf-8 $i > $i.utf8
	touch -r $i $i.utf8
	mv $i.utf8 $i
done

%build
cd CPP/7zip/Compress/LZMA_Alone
make -f makefile.gcc clean all CXX="g++ %{optflags} -fPIC" CXX_C="gcc %{optflags} -fPIC"

%install
mkdir -p %{buildroot}%{_libdir}
install -m0755 CPP/7zip/Compress/LZMA_Alone/liblzmasdk457.so.4.5.7 %{buildroot}%{_libdir}
pushd %{buildroot}%{_libdir}
ln -s liblzmasdk457.so.4.5.7 liblzmasdk457.so.4
ln -s liblzmasdk457.so.4.5.7 liblzmasdk457.so
popd
mkdir -p %{buildroot}/%{_includedir}/lzma457/
find -iname '*.h' | xargs -I {} install -m0644 -D {} %{buildroot}/%{_includedir}/lzma457/{}
magic_rpm_clean.sh

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc lzma.txt history.txt LGPL.txt
%{_libdir}/liblzmasdk457.so.*

%files devel
%doc 7z*.txt Methods.txt
%{_includedir}/lzma457/
%{_libdir}/liblzmasdk457.so

%changelog
* Tue Jul 08 2014 Liu Di <liudidi@gmail.com> - 4.57-4
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.57-3
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.57-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 17 2011 Tom Callaway <spot@fedoraproject.org> - 4.57-1
- make 4.57 package for physfs/physfs2
