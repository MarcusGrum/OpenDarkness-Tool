#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
	Authors:    Marcus Grum, Karsten Tauchert, Norbert Gronau
    Copyright:  University of Potsdam
                Department of Business Informatics, esp. Processes and Systems
	Name:       ShowLicences.py
	Description:
	This opens a window with all the licenc information about the software.
"""

from Tkinter import Toplevel, Text, Scrollbar, Frame, Button

LICENCE = """
OpenDarkness Tool, Support for making decisions for innovations by asking questions.
Copyright (C) 2016/2017 Marcus Grum, Karsten Tauchert, Norbert Gronau

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Contact:
M. Grum, K. Tauchert und N. Gronau
Lehrstuhl fuer Wirtschaftsinformatik, insbesondere Prozesse und Systeme
Universitaet Potsdam
August-Bebel-Straße 89
14482 Potsdam
Telefon: +49 331 977 3379
Fax: +49 331 977 3406
E-Mail: norbert.gronau@wi.uni-potsdam.de
E-Mail: marcus.grum@wi.uni-potsdam.de
E-Mail: karsten.tauchert@wi.uni-potsdam.de
"""

LICENCEUSED = """-------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------

The Python Imaging Library (PIL) is
	Copyright © 1997-2011 by Secret Labs AB
	Copyright © 1995-2011 by Fredrik Lundh
By obtaining, using, and/or copying this software and/or its associated documentation,
you agree that you have read, understood, and will comply with the following terms
and conditions:
Permission to use, copy, modify, and distribute this software and its associated
documentation for any purpose and without fee is hereby granted, provided that
the above copyright notice appears in all copies, and that both that copyright
notice and this permission notice appear in supporting documentation, and that
the name of Secret Labs AB or the author not be used in advertising or publicity
pertaining to distribution of the software without specific, written prior permission.

SECRET LABS AB AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
SECRET LABS AB OR THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL
DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

-------------------------------------------------------------------------------------

PyPDF2 Licence
Copyright (c) 2006-2008, Mathieu Fenniak
Some contributions copyright (c) 2007, Ashish Kulkarni <kulkarni.ashish@gmail.com>
Some contributions copyright (c) 2014, Steve Witham <switham_github@mac-guyver.com>

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

* Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
* The name of the author may not be used to endorse or promote products
  derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

-------------------------------------------------------------------------------------

sshtunnel
Copyright (c) 2014-2016 Pahaz Blinov

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

-------------------------------------------------------------------------------------

matplotlib
John Hunter began matplotlib around 2003. Since shortly before his passing in
2012, Michael Droettboom has been the lead maintainer of matplotlib, but,
as has always been the case, matplotlib is the work of many.
Prior to July of 2013, and the 1.3.0 release, the copyright of the source code
was held by John Hunter. As of July 2013, and the 1.3.0 release, matplotlib
has moved to a shared copyright model.
matplotlib uses a shared copyright model. Each contributor maintains copyright
over their contributions to matplotlib. But, it is important to note that these
contributions are typically only changes to the repositories. Thus, the
matplotlib source code, in its entirety, is not the copyright of any single
person or institution. Instead, it is the collective copyright of the entire
matplotlib Development Team. If individual contributors want to maintain a record
of what changes/contributions they have specific copyright on, they should indicate
their copyright in the commit message of the change, when they commit the change to
one of the matplotlib repositories.
The Matplotlib Development Team is the set of all contributors to the matplotlib
project. A full list can be obtained from the git version control logs.
License agreement for matplotlib 2.0.0

1. This LICENSE AGREEMENT is between the Matplotlib Development Team (“MDT”),
   and the Individual or Organization (“Licensee”) accessing and otherwise using
   matplotlib software in source or binary form and its associated documentation.
2. Subject to the terms and conditions of this License Agreement, MDT hereby grants
   Licensee a nonexclusive, royalty-free, world-wide license to reproduce, analyze,
   test, perform and/or display publicly, prepare derivative works, distribute,
   and otherwise use matplotlib 2.0.0 alone or in any derivative version, provided,
   however, that MDT’s License Agreement and MDT’s notice of copyright, i.e.,
   “Copyright (c) 2012-2013 Matplotlib Development Team; All Rights Reserved” are
   retained in matplotlib 2.0.0 alone or in any derivative version prepared by
   Licensee.
3. In the event Licensee prepares a derivative work that is based on or incorporates
   matplotlib 2.0.0 or any part thereof, and wants to make the derivative work
   available to others as provided herein, then Licensee hereby agrees to include
   in any such work a brief summary of the changes made to matplotlib 2.0.0.
4. MDT is making matplotlib 2.0.0 available to Licensee on an “AS IS” basis. MDT
   MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR IMPLIED. BY WAY OF EXAMPLE,
   BUT NOT LIMITATION, MDT MAKES NO AND DISCLAIMS ANY REPRESENTATION OR WARRANTY OF
   MERCHANTABILITY OR FITNESS FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF MATPLOTLIB
   2.0.0 WILL NOT INFRINGE ANY THIRD PARTY RIGHTS.
5. MDT SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF MATPLOTLIB 2.0.0 FOR ANY
   INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR LOSS AS A RESULT OF MODIFYING,
   DISTRIBUTING, OR OTHERWISE USING MATPLOTLIB 2.0.0, OR ANY DERIVATIVE THEREOF,
   EVEN IF ADVISED OF THE POSSIBILITY THEREOF.
6. This License Agreement will automatically terminate upon a material breach of its
   terms and conditions.
7. Nothing in this License Agreement shall be deemed to create any relationship of
   agency, partnership, or joint venture between MDT and Licensee. This License
   Agreement does not grant permission to use MDT trademarks or trade name in a
   trademark sense to endorse or promote products or services of Licensee, or any
   third party.
8. By copying, installing or otherwise using matplotlib 2.0.0, Licensee agrees to be
   bound by the terms and conditions of this License Agreement.

------------------------------------------------------------------------------------

ReportLab
ReportLab is an Open Source project. Although we are a commercial company we provide
the core PDF generation sources freely, even for commercial purposes, and we make no
income directly from these modules. We also welcome help from the community as much
as any other Open Source project. """

class ShowLicences:
	
	def __init__(self, parent):
		self.parent = parent
		self.showwindow()
		
	def showwindow(self):
		window = Toplevel(self.parent)
		window.title("Lizenzen")
		sbar = Scrollbar(window)
		text = Text(window, height=20, width=100)
		sbar.pack(side='right', fill='y')
		text.pack(side='left', fill='y')
		sbar.config(command=text.yview)
		text.config(yscrollcommand=sbar.set)
		insert = LICENCE + "\n" + LICENCEUSED
		text.insert('end', insert)
